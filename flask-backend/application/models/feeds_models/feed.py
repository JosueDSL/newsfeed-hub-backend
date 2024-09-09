# Desc: Feed model for the application

# Import the database object (db) from the application module
from database import db
from datetime import datetime

class Feed(db.Model):
    """
    Description: This class represents the feed table in the database.

    Attributes:
        id (int): The unique identifier of the feed.
        user_id (int): The user ID of the feed owner.
        name (str): The name of the feed.
        is_public (bool): A flag indicating if the feed is public or private.
        created_at (DateTime): The date and time the feed was created.
        updated_at (DateTime): The date and time the feed was last updated.

    """

    __tablename__ = 'feeds'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Topics and Resources
    topics = db.relationship('Topic', back_populates='feed', lazy=True, cascade="all, delete-orphan")


    # Method to serialize the object data
    def serialize(self):
        """
        Serialize the object instance to a JSON formatted object.

        Returns:
            dict: A dictionary containing the feed data.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'is_public': self.is_public,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
