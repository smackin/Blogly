"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

DEFAULT_URL = 'https://pngimg.com/uploads/snoopy/snoopy_PNG82.png'


def connect_database(app):
    """connect database to Flask app"""
    database.app = app 
    database.init_app(app)
    


class User(database.Model):
    """User info"""
    
    __tablename__ = "users"
    
    user_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    first_name = database.Column(database.Text, nullable=False)
    last_name = database.Column(database.Text, nullable=False)
    image_url = database.Column(database.Text, default=DEFAULT_URL) #may add default image if none
    
    @property
    def full_name(self):
        """return full user name """
        return f"{self.first_name} {self.last_name}"

class Post(database.Model):
    """New Post from User"""
    __tablename__ = 'posts'
    
    post_id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.Text, nullable=False)
    content = database.Column(database.Text, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey(User.user_id), nullable=False)
