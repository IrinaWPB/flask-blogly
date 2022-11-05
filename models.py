"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                           nullable=False)
    image_url = db.Column(db.String(200), 
                          nullable=False,
                          default="static/no_img.jpeg")

    posts = db.relationship("Post", cascade="all, delete")

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"                          

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                           nullable=False)
    content = db.Column(db.String(500),
                           nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)                           
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'),
                          nullable=False)

    created_by = db.relationship('User')
    tags = db.relationship('Tag',
                           secondary='posttags',
                           backref='posts')
    
    
class Tag(db.Model):
    __tablename__ =  'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text, 
                     unique=True,
                     nullable=False)


class PostTag(db.Model):
    __tablename__= 'posttags'

    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id', ondelete='CASCADE'),
                        primary_key=True)
    tag_id = db.Column(db.Integer, 
                        db.ForeignKey('tags.id', ondelete='CASCADE'),
                        primary_key=True)



