from application.services import UserService, AuthService
from unittest.mock import patch

@patch('application.models.User')
def test_register_user(client, app):
    """Test the user registration service logic."""
    with app.app_context():  # Ensure you're in the application context
        payload = {
            'username': 'newuser',
            'password': 'password123'
        }

        user_service = UserService(payload)
        response = user_service.register_user()

        assert response.status_code == 201
        assert b'User registered successfully.' in response.data

@patch('application.models.User')
def test_login_user(client, app):
    with app.app_context(): 
        """Test the user login service logic."""
        payload = {
            'username': 'newuser',
            'password': 'password123'
        }
        
        user_service = AuthService(payload)
        response = user_service.login_user()

        assert response.status_code == 201
        assert b'User logged in successfully.' in response.data