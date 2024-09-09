
# Import flask and the necessary dependencies
from flask import Blueprint, current_app as app, jsonify
from application.blueprints.helper_methods import ErrorHandler
# from services.azure_function_service import AzureFunctionService
from flask_jwt_extended import jwt_required


# Create a blueprint object
feeds_bp = Blueprint('feeds', __name__, url_prefix='/feeds')

# Instantiate the AzureFunctionService with the function URL
# azure_function_service = AzureFunctionService("https://<your-function-app-name>.azurewebsites.net/api/get-new-data")



@feeds_bp.route('/fetch-data', methods=['POST'], endpoint='user_logout')
@ErrorHandler.handle_exceptions
@jwt_required()
async def fetch_news_feed_data_endpoint():

    """
    An asynchronous endpoint to fetch news feeds data from the Azure Function.
    """
    
    # Get the payload from the request
    """
    payload = ErrorHandler.get_json_payload()

    topics = payload.get('topics', ['general'])  # Default to 'general' if no topics provided

    # Use the service class to fetch data from Azure Function asynchronously
    result, status_code = await azure_function_service.fetch_data(topics)

    # Return the response
    return jsonify(result), status_code
    """