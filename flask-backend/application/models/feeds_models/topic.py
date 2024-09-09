# Desc: Topic model for the application

# Import the database object (db) from the application module
from database import db


class Topic(db.Model):
    """
    Description: This class represents the topic table in the database.

    Attributes:
        id (int): The unique identifier of the topic.
        feed_id (int): The feed ID to which the topic belongs.
        name (str): The name of the topic.

    """

    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    """
        Ensure that each topic is unique within a feed
        The constraint "UniqueConstraint" ensures that the combination of feed_id and name is unique.
        It allows the same topic name to exist in different feeds while ensuring that
        each topic name is unique within a single feed. This is useful for scenarios
        where you want to avoid duplicate topic names within the same feed but allow
        the same topic name to be used across different feeds.
    """

    __table_args__ = (db.UniqueConstraint('feed_id', 'name', name='unique_topic_per_feed'),)


    # Relationship to Resources
    feed = db.relationship('Feed', back_populates='topics', lazy=True)


    # Method to serialize the object data
    def serialize(self):
        """
        Serialize the object instance to a JSON formatted object.

        Returns:
            dict: A dictionary containing the topic data.
        """
        return {
            'id': self.id,
            'feed_id': self.feed_id,
            'name': self.name
        }