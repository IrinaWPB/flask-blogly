"""Blogly application."""
import unittest
from flask import Flask, request, render_template, redirect, session
from models import db, connect_db, User, Post, Tag, PostTag
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY']='my_password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/') 
def list_users():
    """Shows List of al users"""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/new')
def show_form():
    """Add user form"""

    return render_template('form.html')

@app.route('/new', methods=["POST"])
def create_user():
    """Adds new user to thge db"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image"]

    new_user = User(first_name=first_name, last_name=last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route('/<int:user_id>', methods=["POST", "GET"])
def show_details(user_id):
    """Show details about that user"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template("details.html",user=user, posts=posts)

@app.route('/<int:user_id>/edit')
def show_edit_form(user_id):
    """Show update form"""

    user = User.query.get(user_id)
    return render_template("edit.html", user=user)
    

@app.route('/<int:user_id>/edit', methods=["POST"])
def edit_info(user_id):
    """Update user info"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image"]
    db.session.commit()
    return redirect('/')

@app.route('/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes user"""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/')


######################POSTS ROUTES########################


@app.route('/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Add post form"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('add_post.html', user=user, tags = tags)

@app.route('/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """Adds new post to thge db"""

    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tag")
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    for tag in tags:
        new_tag = Tag.query.filter_by(name = tag).first()
        new_connection = PostTag(post_id=new_post.id, tag_id = new_tag.id)
        db.session.add(new_connection)
        db.session.commit()

# for tag in tags:
#         new_tag = Tag.query.filter_by(name=tag).first()
#         new_post.append(new_tag)

    return redirect(f"/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows post details"""

    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post = post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show post update form"""

    tags = Tag.query.all()
    post = Post.query.get_or_404(post_id)
    return render_template('update_post.html', post=post, tags=tags)
    

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_submit(post_id):
    """Update post info"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    db.session.commit()
    tags = request.form.getlist("tag")
    
    PostTag.query.filter_by(post_id=post.id).delete()

    for tag in tags:
        new_tag = Tag.query.filter_by(name = tag).first()
        new_connection = PostTag(post_id = post.id, tag_id = new_tag.id)
        db.session.add(new_connection)
        db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Deletes post"""
    post = Post.query.get_or_404(post_id)
    Post.query.filter_by(id = post_id).delete()
    db.session.commit()
    return redirect(f"/{post.user_id}")

#####################Tags ROUTES##########################

@app.route('/tags')
def list_all_tags():
    """Shows all the tags"""

    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Shows a single tag with "edit and "delete" options"""
    
    tag = Tag.query.get_or_404(tag_id)
    
    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new')
def show_add_tag_form():
    """Shows form to create a tag"""

    return render_template('add_tag.html')

@app.route('/tags/new', methods=["POST"])
def add_tag():
    """Creates a new tag"""
    
    name = request.form["name"]
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show edit tag form"""

    tag_to_edit = Tag.query.get(tag_id)

    return render_template('edit_tag.html', tag = tag_to_edit)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """Edit tag"""

    tag_to_edit = Tag.query.get_or_404(tag_id)
    tag_to_edit.name = request.form["name"]
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Deletes the tag with that id"""
    
    Tag.query.filter_by(id = tag_id).delete()
    db.session.commit()

    return redirect('/tags')


