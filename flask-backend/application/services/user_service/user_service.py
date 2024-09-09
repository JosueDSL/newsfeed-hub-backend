# Description: User service class to handle user related operations.

# Import the User model and the database object
from application.models import User
from database import db

# Import the required libraries
from datetime import datetime
from flask import make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies


class UserService:
    """
    User service class to handle user related operations.
    """

    def __init__(self, payload):
        self.payload = payload


    def register_user(self) -> dict:
        """

        Args:
            None    

        Raises:
            ValueError: If the username or password is missing or does not meet the requirements.
        
        Returns:
            JSON: The response JSON with the user details.
        """

        # Validate the payload
        self.validate_payload()

        # Get the username and password from the payload
        username = self.payload['username']
        password = self.payload['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise ValueError('Username already exists. Please choose a different username.')

        # Create a new user object
        new_user = User(username=username)
        
        # Set the password for the new user
        new_user.password = password

        # Set the date of registration as the last login time
        new_user.last_login = datetime.utcnow()
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Log the user after registration
        access_token = create_access_token(identity=new_user.id)

        # Set the JSON response
        response = make_response({
            'id': new_user.id,
            'user': new_user.serialize(),
            'message': 'User registered successfully.'
        }, 201)

        # Set the access token in the response
        set_access_cookies(response, access_token)

        return response


    def login_user(self):
        """
        Authenticates a user and generates a JWT token.

        Raises:
            ValueError: If the username or password is incorrect.

        Returns:
            JSON: The response JSON with the JWT token.
        """
        # Validate the payload
        self.validate_payload()

        # Get the username and password from the payload
        username = self.payload['username']
        password = self.payload['password']

        # Find the user by username
        user = self.get_user(username)
        if not user:
            raise ValueError('Invalid username.')
        
        # Verify the password
        if not user.verify_password(password):
            raise ValueError('Invalid password.')

        # Update the last login time
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Create a JWT token
        access_token = create_access_token(identity=user.id)

        # Set the JSON response
        response = make_response({
            'user_id': user.id,
            'username': user.username,
            'message': 'User logged in successfully.'
        }, 201)

        # Set the access token in the response
        set_access_cookies(response, access_token)

        return response


    def logout_user(self):
        """
        Logs out the user by clearing the JWT token.

        Returns:
            JSON: The response JSON with the message.
        """
        # Set the JSON response
        response = make_response({
            'message': 'User logged out successfully.'
        }, 200)

        # Clear the JWT cookies in the response
        unset_jwt_cookies(response)

        return response


    def get_user(self, username: str) -> User:
        """
        Get the user by username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The user object.
        """
        return User.query.filter_by(username=username).first()


    def validate_payload(self) -> None:
        """ Validate the payload for the user service. 
        
        Args:
            None

        Raises:
            ValueError: If the username or password is missing or does not meet the requirements.
        """
        username = self.payload.get('username')
        password = self.payload.get('password')

        # Check if the username and password are provided and meet the requirements
        if not username or not password:
            raise ValueError('Username and password are required.')
        elif len(username) < 4 or len(username) > 50:
            raise ValueError('Username must be between 4 and 50 characters long.')
        elif len(password) < 8 or len(password) > 50:
            raise ValueError('Password must be between 8 and 50 characters long.')

        # Safely convert username and password to strings
        self.payload['username'] = str(username)
        self.payload['password'] = str(password)