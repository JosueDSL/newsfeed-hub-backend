import json

def test_create_feed(client):
    # Simulate user login to obtain a JWT token and CSRF token
    login_payload = {
        'username': 'kiosko',
        'password': 'kiosko'
    }
    login_response = client.post('/auth/login', data=json.dumps(login_payload), content_type='application/json')

    # Extract JWT and CSRF token from cookies
    csrf_token = login_response.cookies.get('csrf_access_token')
    jwt_token = login_response.cookies.get('access_token_cookie')

    print(f'CSRF token: {csrf_token}')
    print(f'JWT token: {jwt_token}')

    assert csrf_token is not None, "CSRF token not found in cookies"
    assert jwt_token is not None, "JWT token not found in cookies"

    # Now use the tokens to create a feed
    payload = {
        'name': 'Sports Feed',
        'topics': ['swimming', 'cycling', 'tennis']
    }

    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-CSRF-TOKEN': csrf_token
    }
    response = client.post('/feeds/create-feed', data=json.dumps(payload), content_type='application/json', headers=headers)
    
    assert response.status_code == 201


def test_feed_listing(client):
    """Test listing feeds."""
    # Create a feed first
    test_create_feed(client)

    # Now list the feeds
    response = client.get('/feeds/list', content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['feeds']) > 0
    assert 'Sports Feed' in data['feeds'][0]['name']
