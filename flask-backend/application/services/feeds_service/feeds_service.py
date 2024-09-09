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