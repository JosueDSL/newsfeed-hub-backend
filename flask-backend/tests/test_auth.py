import json

def test_user_registration(client):
    """Test the user registration endpoint."""
    payload = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    response = client.post('/user/register', data=json.dumps(payload), content_type='application/json')
    
    # Check if the status code is 201 (created)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'User registered successfully.'
    assert 'id' in data['user']

def test_user_login(client):
    """Test the user login endpoint."""
    # First, register the user
    test_user_registration(client)

    # Then, attempt to log in with the same credentials
    payload = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    response = client.post('/auth/login', data=json.dumps(payload), content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'user_id' in data
    assert data['message'] == 'User logged in successfully.'


