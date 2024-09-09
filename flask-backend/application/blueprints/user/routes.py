# Import flask and the necessary dependencies
from flask import Blueprint, request

# Import the required libraries
from application.blueprints.helper_methods import ErrorHandler
from application.services import UserService



# Create a blueprint object
user_bp = Blueprint('user', __name__)


# Health check route
@user_bp.route('/health', methods=['GET'])
def health():
    return 'OK', 200


# User registration route
@user_bp.route('/register', methods=['POST'], endpoint='user_register')
@ErrorHandler.handle_exceptions
def register_user_endpoint():
    # Get the payload from the request
    payload = ErrorHandler.get_json_payload()

    # Create a new user service object
    user_service = UserService(payload)

    # Register the user
    response = user_service.register_user()

    return response
