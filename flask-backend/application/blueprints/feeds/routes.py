
# Import flask and the necessary dependencies
from flask import Blueprint, current_app as app, jsonify, request
from application.blueprints.helper_methods import ErrorHandler
from flask_jwt_extended import jwt_required
from application.services import FeedDataHandler, AzureFunctionService


# Create a blueprint object
feeds_bp = Blueprint('feeds', __name__, url_prefix='/feeds')


@feeds_bp.route('/create-feed', methods=['POST'], endpoint='user_logout')
@ErrorHandler.handle_exceptions
@jwt_required()
async def fetch_news_feed_data_endpoint():

    """
    An asynchronous endpoint to fetch news feeds data from the Azure Function.
    """
    
    # Get the payload from the request

    payload = ErrorHandler.get_json_payload()

    feed = FeedDataHandler(payload)

    # Process the request
    response = await feed.process_request()

    # Return the response
    return jsonify(response), 200



@feeds_bp.route('/test-azure-func', methods=['POST'], endpoint='test_azure_func')
@ErrorHandler.handle_exceptions
@jwt_required()
async def test_azure_func():
    """
    An asynchronous endpoint to test the Azure Function.
    """

    # Get the payload from the request
    payload = ErrorHandler.get_json_payload()


    app.logger.info(f"Payload received: {payload}")
    
    app.logger.info(app.config['AZURE_FUNCTION_URL'])

    # Initialize the AzureFunctionService with the Azure Function URL
    azure_func = AzureFunctionService(app.config['AZURE_FUNCTION_URL'])

    # Process the request
    response = await azure_func.fetch_data(payload["topics"])

    # Return the response
    return jsonify(response), 200

