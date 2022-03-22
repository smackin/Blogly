from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import database, connect_database, User
import pdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'illnevertell'

toolbar = DebugToolbarExtension(app)

connect_database(app)
database.create_all()

@app.route('/')
def show_home():
    """show form to enter into db"""
    
    return render_template('base.html')


@app.route('/users')
def users_index():
    """Show a page with info on all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_users_form():
    """Show a form to create a new user"""
    return render_template('new.html')

@app.route("/users/new", methods=["POST"])
def create_user():
    """post to create the user and commit to db"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    user_img = request.form["image_url"]
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=user_img)
    database.session.add(new_user)
    database.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_users(user_id):
    """ show list of all users in DB"""
    user = User.query.get(user_id)
    return render_template ('show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """use form to edit existing user"""
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)
    
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """submit updated user information. form submission"""
    user = User.query.get(user_id)
    user.first_name = request.form["first"]
    user.last_name = request.form["last"]
    user.user_img = request.form["image"]
    
    database.session.add(user)
    database.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    
    user = User.query.get(user_id)
    database.session.delete(user)
    database.session.commit()
    
    return redirect("/users")


