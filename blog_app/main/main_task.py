from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, \
     jsonify, abort, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from ..main import main
from ..models import User, Post, db
from ..valids import *

@main.route('/')
@main.route('/resume')
def show_resume():
    return render_template("resume.html")

#@main.route('/')
#def hello():
 #   return render_template("welcome.html")
    #return render_template("portfolio.html")

@main.route('/portfolio')
def about():
    #return render_template("about_me.html")
    return render_template("portfolio.html")

@main.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username = username, username_logged = username)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and user.username == username and user.verify_password(password):
                #return render_template('welcome.html', username=user.username)
                session['logged_in'] = True
                flash("You were logged in")
                session['username'] = username
                return redirect(url_for('main.welcome', username=username))
            else:
                error = "This user is invalid"
                return render_template('login.html', error = error)

        else:
            error = "You need to input both username and password"
            return render_template('login.html', error = error)
    else:
        return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    session['username'] = ""
    flash("You were logged out")
    return redirect(url_for('post.show_all_posts'))

@main.route('/signup', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirm = request.form['password_confirm']

        valid_usernames = valid_username(username)
        valid_passwords = valid_password(password)
        valid_emails = valid_email(email)
        have_error = False

        params = dict(username = username, email = email)

        if not valid_usernames:
            params['error_username'] = "This username is invalid!"
            have_error = True
        else:
            all_username = User.query.with_entities(User.username).all()
            if all_username:
                if (username,) in all_username:
                    params['error_username'] = "This username already exists"
                    have_error = True

        if not valid_passwords:
            params['error_password'] = "This password is invalid!"
            have_error = True

        if email and not valid_emails:
            params['error_email'] = "This email is invalid!"
            have_error = True

        if (not confirm) and valid_passwords:
            params['error_confirm'] = "Please confirm your password!"
            have_error = True

        if valid_passwords and confirm and (password != confirm):
            params['error_confirm'] = "Confrim not match with password!"
            have_error = True

        if have_error == True:
            #return redirect("signup.html", **params)
            return render_template('signup.html', **params)
        else:
            params = dict(username = username,
                          password = password,
                          email = email)
            #newUser = User(username = username, password = password, email = email)
            """
                **params: pass a dict of params to function
                *params: pass a list of params to function
            """
            newUser = User(**params)
            db.session.add(newUser)
            db.session.commit()
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('main.welcome', username=username))

    else:
        return render_template('signup.html')
