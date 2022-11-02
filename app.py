"""Blogly application."""

from flask import Flask, request, render_template, redirect, session
from models import db, connect_db, User

app = Flask(__name__)

app.config['SECRET_KEY']='my_password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

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
    image_url = image_url if image_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route('/<int:user_id>')
def show_details(user_id):
    """Show details about that user"""

    user = User.query.get_or_404(user_id)
    return render_template("details.html",user=user)

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
