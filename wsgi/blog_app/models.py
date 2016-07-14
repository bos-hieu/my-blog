from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
#from .app_factory import db


db = SQLAlchemy()

class User(db.Model):
    _tablename__ = 'user'
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(60))
    posts = db.relationship('Post', backref='user')

    def __init__(self, username,password, email = ""):
        self.username = username
        self.password = password
        self.email = email

    """@property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)"""
    

        
class Post(db.Model):
    _tablename__ = 'post'
    id = db.Column('post_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    content = db.Column(db.TEXT)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.pub_date = datetime.utcnow()
