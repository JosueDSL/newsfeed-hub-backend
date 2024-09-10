
# Import flask and the necessary dependencies
from flask import Blueprint, current_app as app, jsonify, request
from application.blueprints.helper_methods import ErrorHandler
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.services import FeedDataHandler, PaginationService, FeedsService, AzureFunctionService


# Create a blueprint object
feeds_bp = Blueprint('feeds', __name__, url_prefix='/feeds')


@feeds_bp.route('/create-feed', methods=['POST'], endpoint='create_feed')
@ErrorHandler.handle_exceptions
@jwt_required()
async def fetch_news_feed_data_endpoint():

    """
    An asynchronous endpoint to fetch news feeds data from the Azure Function.

    Args:
        payload (dict): The payload containing the topics to fetch.

    Returns:
        JSON: The response from the Azure Function.

    """
    
    # Get the payload from the request

    payload = ErrorHandler.get_json_payload()

    feed = FeedDataHandler(payload)

    # Process the request
    response = await feed.process_request()

    # Return the response
    return jsonify(response), 200



@feeds_bp.route('/list', methods=['GET'], endpoint='list_feeds')
@ErrorHandler.handle_exceptions
@jwt_required()
def list_feeds_endpoint():
    """
    List the private feeds of the current user, with pagination and sorting by update/creation date.

    Args:
        page (int): The page number for pagination.
        per_page (int): The number of items per page for pagination.

    Returns:
        JSON: The serialized paginated private feeds.
    """
    current_user_id = get_jwt_identity()

    # Get pagination params (default 1st page, 10 items per page)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Initialize the pagination service
    pagination_service = PaginationService(page=page, per_page=per_page)

    # Get paginated and serialized private feeds
    paginated_feeds = pagination_service.get_paginated_feeds(user_id=current_user_id)

    # Return the serialized paginated feeds
    return jsonify(paginated_feeds), 200



@feeds_bp.route('/list-public', methods=['GET'], endpoint='list_public_feeds')
@ErrorHandler.handle_exceptions
def list_public_feeds_endpoint():

    """
    List public feeds with optional topic filter, with pagination and sorting by update/creation date.

    Args:
        page (int): The page number for pagination.
        per_page (int): The number of items per page for pagination.
        topic_filter (str): The topic filter to apply to the feeds.

    Returns:
        JSON: The serialized paginated

    """
    # Get pagination params (default 1st page, 10 items per page)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    topic_filter = request.args.get('topic', None)

    # Initialize the pagination service
    pagination_service = PaginationService(page=page, per_page=per_page)

    # Get paginated and serialized public feeds, optionally filtered by topic
    paginated_feeds = pagination_service.get_paginated_feeds(is_public=True, topic_filter=topic_filter)

    # Return the serialized paginated feeds
    return jsonify(paginated_feeds), 200


@feeds_bp.route('/details/<int:feed_id>', methods=['GET'], endpoint='feed_details')
@ErrorHandler.handle_exceptions
def feed_details_endpoint(feed_id):

    """
    Get details of a specific feed, including its topics and resources (paginated).

    Args:
        feed_id (int): The ID of the feed to get details for.

    Returns:
        JSON: The serialized feed details.

    """
    # Initialize the pagination service
    pagination_service = PaginationService()

    # Get the serialized feed details, including topics and resources
    feed_details = pagination_service.get_feed_details(feed_id)

    # Return the serialized feed details
    return jsonify(feed_details), 200


@feeds_bp.route('/<int:feed_id>', methods=['PUT'], endpoint='update_feed')
@ErrorHandler.handle_exceptions
@jwt_required()
def update_feed_endpoint(feed_id):
    """
    Update an existing feed in the database.

    Args:
        feed_id (int): The ID of the feed to update.
        payload (dict): The payload to update the feed with.

    Returns:
        JSON: The updated feed object.

    """

    # Get the payload from the request
    payload = ErrorHandler.get_json_payload()

    # Update the feed using the service method
    response = FeedsService.update_feed(feed_id, payload)

    return jsonify(response), 200



@feeds_bp.route('/<int:feed_id>', methods=['DELETE'], endpoint='delete_feed')
@ErrorHandler.handle_exceptions
@jwt_required()
def delete_feed_endpoint(feed_id):
    """
    Delete an existing feed from the database.

    Args:
        feed_id (int): The ID of the feed to delete.

    Returns:
        JSON: A success message.
    """

    # Delete the feed using the service method
    response = FeedsService.delete_feed(feed_id)

    return jsonify(response), 200



@feeds_bp.route('/test-azure-func', methods=['POST'], endpoint='test_azure_func')
@ErrorHandler.handle_exceptions
@jwt_required()
async def test_azure_func_endpoint():
    """
    An asynchronous endpoint to test the Azure Function.

    Args:
        payload (dict): The payload containing the topics to fetch.

    Returns:
        JSON: The response from the Azure Function.
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

