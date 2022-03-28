"""Seed file to make users table """

from models import User, database
from app import app


# create all tables 

database.drop_all()
database.create_all()

bob = User(first_name='Bob', last_name='Roberts', image_url='https://pngimg.com/uploads/snoopy/snoopy_PNG82.png')
steph = User(first_name='Stephanie', last_name='Mackin', image_url='https://pngimg.com/uploads/snoopy/snoopy_PNG82.png')
sam = User(first_name='Sammie', last_name='Girl', image_url='https://pngimg.com/uploads/snoopy/snoopy_PNG82.png')
zach = User(first_name='Zach', last_name='Gumby', image_url='https://pngimg.com/uploads/snoopy/snoopy_PNG82.png')

database.session.add_all([bob, steph, sam, zach])
database.session.commit()