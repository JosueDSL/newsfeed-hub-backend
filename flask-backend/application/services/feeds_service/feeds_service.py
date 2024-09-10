# Description: Service layer for the feeds resource.

# Import the necessary modules
from database import db
from application.models import Feed
from flask_jwt_extended import get_jwt_identity
from datetime import datetime

class FeedsService:
    """
    A service class to interact with the feeds in the database.
    """

    @staticmethod
    def insert_feed(feed_name: str, is_public: bool) -> Feed:
        """
        Insert a new feed into the database.

        Args:
            feed_name (str): The name of the feed.
            is_public (bool): Whether the feed is public or not.

        Returns:
            Feed: The newly created feed object.
        """
        # Get the user ID from the JWT token
        user_id = get_jwt_identity()

        # Create the feed object
        new_feed = Feed(name=feed_name, is_public=is_public, user_id=user_id)

        # Add the feed to the database and flush the session
        db.session.add(new_feed)

        # Commit all the updates to the session database
        db.session.commit()

        return new_feed


    @staticmethod
    def update_feed(feed_id, payload) -> dict:
        """
        Update an existing feed in the database.

        Args:
            feed_id (int): The ID of the feed to update.
            payload (dict): The payload to update the feed with.

        Returns:
            Feed: The updated feed object.

        Raises:
            ValueError: If the feed is not found.
        """
        # Ensure payload is provided
        print(f"Payload: {payload}")
        if not payload:
            raise ValueError('Payload is required')

        elif not isinstance(payload, dict):
            raise ValueError('Payload must be a dictionary')

        # Ensure feed_id is provided and valid
        if feed_id is None:
            raise ValueError('Feed ID is required')

        if not isinstance(feed_id, int):
            raise ValueError('Feed ID must be an integer')


        # Get the feed by ID
        feed = Feed.query.get(feed_id)

        if not feed:
            raise ValueError('Feed not found')
        
        # Ensure the user is the owner of the feed
        user_id = get_jwt_identity()
        if feed.user_id != user_id:
            raise ValueError('Unauthorized to update this feed')

        # Update feed attributes if provided
        feed_name = payload.get('feed_name')
        if not isinstance(feed_name, str):
            raise ValueError('feed_name must be a string')

        is_public = payload.get('is_public')
        if not isinstance(is_public, bool):
            raise ValueError('is_public must be a boolean')

        if feed_name:
            feed.name = feed_name
        if is_public is not None:
            feed.is_public = is_public


        # Commit changes to the database
        db.session.commit()


        response = {
            'id': feed.id,
            'name': feed.name,
            'is_public': feed.is_public,
            'topics': [topic.name for topic in feed.topics],
            'updated_at': feed.updated_at
        }

        return response