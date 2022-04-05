from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import database, connect_database, User, Post, Tag
import pdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'illnevertell'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_database(app)
database.create_all()

@app.route('/')
def show_home():
    """display home page with list of users to select """
    posts = Post.query.all()
    return render_template('home_posts.html', posts=posts)

##### User routes - singup, delete, show all ####
@app.route('/users')
def users_index():
    """Show a page with info on all users"""

    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_users_form():
    """Show a form to create a new user"""
    return render_template('new.html')

@app.route("/users/new", methods=["POST"])
def create_user():
    """post to create the user and commit to database"""
    new_user = User(
        first_name=request.form["first_name"],
        last_name=request.form["last_name"] ,
        image_url=request.form["image_url"] or None)
        
    database.session.add(new_user)
    database.session.commit()
    flash(f"User '{new_user.first_name}' is now in our database!" )
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_users(user_id):
    """ show list of all users in database"""
    user = User.query.get_or_404(user_id)
    return render_template ('show_user.html', user=user, post=post_id)

@app.route('/users/<int:user_id>/edit') 
def edit_user(user_id):
    """display form to edit existing user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)
    
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """submit updated user information. form submission"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    
    database.session.add(user)
    database.session.commit()
    flash(f"User '{user.first_name}' has been updated.")

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """form submission to delete an existing user"""
    user = User.query.get(user_id)
    database.session.delete(user)
    database.session.commit()
    
    return redirect("/users")


#### Post routes - Created by Users #### 

@app.route('/users/<int:user_id>/posts/new')
def user_new_post_form(user_id):
    """display form to add a new post for user """
    
    user = User.query.get_or_404(user_id)
    return render_template('new_posts.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    """form submission to add post for a user """
    user = User.query.get_or_404(user_id)
    
    new_post = Post(
        title = request.form['title'],
        content = request.form['content'],
        user_id = user_id)
    
    database.session.add(new_post)
    database.session.commit()
    
    return redirect(f"/users/{user_id}")



@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    database.session.add(post)
    database.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    database.session.delete(post)
    database.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")


##############################################################################
# User and Post Tags route


@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    database.session.add(new_tag)
    database.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    database.session.add(tag)
    database.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    database.session.delete(tag)
    database.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")