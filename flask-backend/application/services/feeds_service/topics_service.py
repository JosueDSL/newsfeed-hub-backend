# Description: Service layer for the topics resource.

# Import the necessary modules
from database import db
from application.models import Topic, Feed


class TopicService:
    @staticmethod
    def insert_feed_topic(topic: str, feed_id: int) -> Topic:
        """
        Insert a new topic into the database.

        Args:
            topic (str): The topic to add.
            feed_id (int): The feed ID to which the topic belongs.

        Returns:
            Topic: The newly created topic object.

        Raises:
            ValueError: If the number of topics exceeds the limit
            or invalid input provided.
        """
        TopicService._validate_topic(topic, feed_id)

        # Get the current topics
        current_topics = TopicService.get_topics(feed_id)
        if len(current_topics) >= 5:
            raise ValueError('Cannot add more than 5 topics per feed.')

        # Create the topic object
        new_topic = Topic(name=topic, feed_id=feed_id)

        # Add the topic to the database
        db.session.add(new_topic)

        return new_topic


    @staticmethod
    def get_topics(feed_id: int) -> list:
        """
        Get the list of topics related to the feed.

        Args:
            feed_id (int): The feed ID to get topics for.

        Returns:
            list: A list of topic names.
        """
        # Get the feed object
        feed = Feed.query.get(feed_id)
        if not feed:
            raise ValueError('Feed not found.')

        # Query all the topics related to the feed
        topics = Topic.query.filter_by(feed_id=feed_id).all()
        if not topics:
            return []

        # Get the topic names
        topic_names = [topic.name for topic in topics]

        return topic_names


    @staticmethod
    def _validate_topic(topic: str, feed_id: int) -> None:
        """
        Private method that validates the topic and feed ID before adding the topic.

        Args:
            topic (str): The topic to add.
            feed_id (int): The feed ID to which the topic belongs.

        Raises: 
            ValueError: If the topic or feed ID is invalid.
        """
        # Ensure the feed_id is valid
        if not feed_id or not topic:
            raise ValueError('A topic and feed ID must be provided.')
        if not str(feed_id).isdigit():
            raise ValueError('Invalid feed ID, it must be a number.')

        try:
            # Convert feed_id to an integer
            feed_id = int(feed_id)
            # Convert the topic to a string
            topic = str(topic)
        except ValueError:
            raise ValueError('Invalid feed ID or topic.')

        # Validate topic length
        if len(topic) > 50:
            raise ValueError('Topic name must be less than 50 characters.')
        elif len(topic) < 3:
            raise ValueError('Topic name must be at least 3 characters.')