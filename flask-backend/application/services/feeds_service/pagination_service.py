from application.models import Feed, Topic, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request


class PaginationService:
    def __init__(self, page=1, per_page=10):
        self.page = page
        self.per_page = per_page


    def get_paginated_feeds(self, user_id=None, is_public=None, topic_filter=None):
        """
        Fetch and paginate feeds based on the provided parameters.

        Args:
            user_id (int): Filter feeds by user_id (for private feeds).
            is_public (bool): Filter feeds by public status (True for public, False for private).
            topic_filter (str): Filter feeds by topic.

        Returns:
            dict: Serialized paginated feeds and pagination details.
        """
        # Start a base query
        query = Feed.query

        # Filter by user_id if provided (for private feeds)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)

        # Filter by public status if provided
        if is_public is not None:
            query = query.filter_by(is_public=is_public)

        # Apply topic filter if provided
        if topic_filter:
            query = query.join(Topic).filter(Topic.name.ilike(f"%{topic_filter}%"))

        # Paginate the query results
        paginated_feeds = query.order_by(Feed.updated_at.desc()).paginate(page=self.page, per_page=self.per_page, error_out=False)

        # Serialize the feeds and pagination details
        feeds = [{
            "name": feed.name,
            "creator": feed.user.username if is_public else None,
            "is_public": feed.is_public,
            "topics": [topic.name for topic in feed.topics],
            "created_at": feed.created_at,
            "updated_at": feed.updated_at
        } for feed in paginated_feeds.items]

        return {
            "feeds": feeds,
            "page": paginated_feeds.page,
            "pages": paginated_feeds.pages
        }


    def get_feed_details(self, feed_id):
        """
        Get detailed information about a specific feed, including its topics and resources.
        Paginate the resources (limit to 20 most recent).

        Args:
            feed_id (int): The ID of the feed to fetch.

        Returns:
            dict: Serialized feed details and resources.
        """
        # Fetch the feed
        feed = Feed.query.get_or_404(feed_id)

        # Ensure the JWT is verified before accessing JWT-dependent methods
        verify_jwt_in_request()

        # Now you can safely call get_jwt_identity()
        user_id = get_jwt_identity()
        print(f"User ID: {user_id}")
        print(f"Feed User ID: {feed.user_id}")

        # Ensure the feed is public or belongs to the current user
        if not feed.is_public and feed.user_id != user_id:
            raise ValueError("You do not have permission to view this feed.")

        # Serialize feed details
        feed_details = {
            "name": feed.name,
            "is_public": feed.is_public,
            "topics": [topic.name for topic in feed.topics],
            "created_at": feed.created_at,
            "updated_at": feed.updated_at,
            "resources": []
        }

        # Get the resources (limit to 20 most recent)
        for topic in feed.topics:
            resources = Resource.query.filter_by(topic_id=topic.id).order_by(Resource.date.desc()).limit(20).all()
            serialized_resources = [{
                "title": resource.title,
                "date": resource.date,
                "type": resource.type,
                "editorial": resource.editorial,
                "languages": resource.languages
            } for resource in resources]
            feed_details["resources"].extend(serialized_resources)

        return feed_details
