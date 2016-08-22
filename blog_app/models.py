from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Role(db.Model):
    __tablename__ ='roles'
    id = db.Column(db.Integer, primary_key = True)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(60))
    registered_date = db.Column(db.DateTime)
    posts = db.relationship('Posts', backref='users')

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


posts_tags = db.Table('posts_tags',
                      db.Column('post_id', db.Integer, db.ForeignKey('posts.post_id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id')),
                      db.PrimaryKeyConstraint('post_id', 'tag_id'))


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column('post_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    content = db.Column(db.TEXT)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    tags = db.relationship('Tags', secondary = posts_tags, backref = 'posts')
    comments = db.relationship('Comments', backref='posts')

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
            'user_id': self.user_id,
            'category_id': self.category_id
            }


class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column('tag_id', db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    #posts_t = db.relationship('Posts', secondary = posts_tags, backref = 'tags')

    def __init__(self, name):
        self.name = name


class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column('category_id', db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    posts = db.relationship('Posts', backref='categories')

    def __init__(self, name):
        self.name = name


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column('comment_id', db.Integer, primary_key=True)
    author = db.Column(db.String(60))
    content = db.Column(db.String(250))
    pub_date = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))

    def __init__(self, author, content):
        self.author = author
        self.content = content
        self.pub_date = datetime.utcnow()

    @property
    def serialize(self):

        return {
            'comment_id': self.id,
            'author': self.author,
            'content': self.content,
            'pub_date': self.pub_date,
            'post_id': self.post_id
            }
