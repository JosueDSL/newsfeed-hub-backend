# Description: This file contains the User class which represents the user table in the database.

# Import the required modules
from database import db
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash



class User(db.Model, UserMixin):
    """
    Description: This class represents the user table in the database.
    
    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        password_hash (str): The hashed password of the user.
        last_login (DateTime): The date and time of the user's last login.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime)


    # Set the password attribute to be write-only
    @property
    def password(self):
        """
        Prevents reading the password attribute.
        
        Raises:
            AttributeError: Always raises an AttributeError to prevent reading the password.
        """
        raise AttributeError('password is not a readable attribute')


    @password.setter
    def password(self, password: str) -> None:
        """
        Hashes the password and stores it in the password_hash attribute.
        
        Args:
            password (str): The plaintext password to be hashed.
        """
        self.password_hash = generate_password_hash(password).decode('utf8')


    def verify_password(self, password: str) -> bool:
        """
        Verifies the provided password against the stored password hash.
        
        Args:
            password (str): The plaintext password to verify.
        
        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        return check_password_hash(self.password_hash, password)


    # Serialize the object instance to a JSON formatted object
    def serialize(self):
        """
        Serializes the user object to a JSON-compatible dictionary.
        
        Returns:
            dict: A dictionary containing the user's id, username, and last login time.
        """
        return {
            'id': self.id,
            'username': self.username,
            'last_login': self.last_login
        }