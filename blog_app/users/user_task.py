from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, \
     jsonify, abort, escape, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from ..users import user
from ..models import User, Post, db
from ..decorators import login_required
from ..valids import *


@user.route('/<username>/profile')
@login_required
def user_profile(username):
    current_user = User.query.filter_by(username=username).one()
    return render_template("show_profile.html", current_user = current_user)
    

@user.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    '''Edit profile of user'''
    
    edited_profile = User.query.filter_by(id=user_id).one()

    if request.method == 'POST':
        username = request.form['username']
        #email = request.form['email']
        email = request.form['email']
        if valid_username(username) and valid_email(email):
            edited_profile.username = username
            edited_profile.email = email
            db.session.add(edited_profile)
            db.session.commit()
            session['username'] = username
            return redirect(url_for('user.user_profile', username = username))
        else:
            return render_template("edit_profile.html",
                                   current_user = edited_profile)
    else:
        return render_template("edit_profile.html",
                               current_user = edited_profile)

@user.route('/<int:user_id>/resetpassword')
def reset_password(user_id):
    edited_profile = User.query.filter_by(id=user_id).one()
    return render_template("reset_password.html",current_user = edited_profile)

@user.route('/<int:user_id>/posts')
@login_required
def show_user_posts(user_id):
    '''Show all posts of user'''

    user_posts = Post.query.filter_by(user_id=user_id).all()

    return render_template('user_posts.html', posts = user_posts)

@user.route('s/JSON')
def users_JSON():
    users = db.session.query(User).all()
    
    return jsonify(Users = [i.serialize for i in users])

@user.route('/<int:user_id>/JSON')
def user_JSON(user_id):
    user = User.query.filter_by(id=user_id).one()
    
    return jsonify(user = user.serialize)


