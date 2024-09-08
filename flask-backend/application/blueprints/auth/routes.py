# Import flask and the necessary dependencies
from flask import Blueprint

# Create a blueprint object
auth_bp = Blueprint('auth', __name__)


# Health check route
@auth_bp.route('/health', methods=['GET'])
def health():
    return 'OK', 200