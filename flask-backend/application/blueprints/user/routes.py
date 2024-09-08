# Import flask and the necessary dependencies
from flask import Blueprint

# Create a blueprint object
user_bp = Blueprint('user', __name__)


# Health check route
@user_bp.route('/health', methods=['GET'])
def health():
    return 'OK', 200