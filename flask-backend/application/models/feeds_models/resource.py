# Desc: Resource model for the application

# Import the database object (db) from the application module
from database import db


class Resource(db.Model):
    """
    Description: This class represents the resource table in the database.

    Attributes:
        id (int): The unique identifier of the resource.
        feed_id (int): The feed ID to which the resource belongs.
        title (str): The title of the resource.
        date (str): The date of the resource.
        type (str): The type of the resource.
        editorial (str): The editorial of the resource.
        languages (str): The languages of the resource.
    """

    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100))
    editorial = db.Column(db.String(255))
    languages = db.Column(db.String(255))

    # Relationship to Feed
    feed = db.relationship('Feed', backref='resources', lazy=True)

    # Method to serialize the object data
    def serialize(self):
        """
        Serialize the object instance to a JSON formatted object.

        Returns:
            dict: A dictionary containing the resource data.
        """
        return {
            'id': self.id,
            'feed_id': self.feed_id,
            'title': self.title,
            'date': self.date,
            'type': self.type,
            'editorial': self.editorial,
            'languages': self.languages
        }

