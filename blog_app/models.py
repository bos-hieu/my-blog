from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Role(db.Model):
    __tablename__ ='roles'
    id = db.Column(db.Integer, primary_key = True)
    

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(60))
    registered_date = db.Column(db.DateTime)
    posts = db.relationship('Post', backref='user')

    def __init__(self, username,password, email = ""):
        self.username = username
        self.password = password
        self.email = email
        self.registered_date = datetime.utcnow()

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def serialize(self):

        return {
            'user_id': self.id,
            'username': self.username,
            'email': self.email,
            'registered': self.registered_date
            }

      
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column('post_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    content = db.Column(db.TEXT)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.pub_date = datetime.utcnow()

    @property
    def serialize(self):

        return {
            'post_id': self.id,
            'title': self.title,
            'content': self.content,
            'pub_date': self.pub_date,
            'user_id': self.user_id
            }
