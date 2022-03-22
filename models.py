"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

DEFAULT_IMG_URL = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.istockphoto.com%2Fillustrations%2Ficon-silhouettes&psig=AOvVaw2tuGFIkr86jKCzALKTr6gX&ust=1647705564216000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCLDIo-CD0PYCFQAAAAAdAAAAABAD"

class User(database.Model):
    """User info"""
    
    __tablename__ = "users"
    
    userid = database.Column(database.Integer, primary_key=True, autoincrement=True)
    first_name = database.Column(database.Text, nullable=False)
    last_name = database.Column(database.Text, nullable=False)
    image_url = database.Column(database.Text, nullable=False, default=DEFAULT_IMG_URL) #may add default image if none
    

#     def greet_user(self):
#         return f" Hey there {self.first_name} {self.last_name}"

def connect_database(app):
    """connect database to Flask app"""
    database.app = app 
    database.init_app(app)
    
    database.app = app 
    database.init_app(app)
    
    