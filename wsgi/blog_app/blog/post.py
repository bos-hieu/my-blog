from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from ..blog import blog
from ..models import User, Post, db


@blog.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            user = User.query.filter_by(username=username).one()
            if user.username == username and user.password == password:
                return render_template('welcome.html', username=user.username)
            else:
                error = "This user is invalid"
                return render_template('login.html', error = error)
        else:
            error = "You need to input both username and password"
            return render_template('login.html', error = error)
    else:
        return render_template('login.html')


@blog.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username and password:
            newUser = User(username = username, password = password, email = email)
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('main.hello'))
        else:
            error = "You need to input both usernam and password"
            return render_template('signup.html', error = error)
    else:
        return render_template('signup.html')


@blog.route('/post')
def all_posts():
    ''''Show all post of blog'''

    posts = Post.query.order_by(Post.pub_date.desc()).all()
    return render_template("allpost.html", posts = posts)


@blog.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.filter_by(id=post_id).one()
    return render_template("post.html", post = post)


@blog.route('/newpost', methods=['GET','POST'])
def new_post():
    ''''Create a new post'''

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error = "We need both a title and some content!"
        if title and content:
            newPost = Post(title = title, content = content.replace("\n", "<br>"))
            db.session.add(newPost)
            db.session.commit()
            return redirect(url_for('blog.show_post',post_id = newPost.id))
        else:
            return render_template('newpost.html', error = error)
    else:
        return render_template('newpost.html')

@blog.route('/edit/post/<int:post_id>', methods=['GET','POST'])
def edit_post(post_id):
    ''''edit a post'''

    edited_post = Post.query.filter_by(id=post_id).one()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error = "We need both a title and some content!"
        if title and content:
            edited_post.title = title
            edited_post.content = content
            edited_post.pub_date = datetime.utcnow()
            db.session.add(edited_post)
            db.session.commit()
            return redirect(url_for('blog.show_post',post_id = edited_post.id))
        else:
            return render_template('editpost.html', error = error)
    else:
        return render_template('editpost.html', post_id = post_id, post = edited_post)

@blog.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    if request.method == 'POST':
        post = Post.query.filter_by(id=post_id).one()
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('blog.all_posts'))
    else:
        return render_template('delete.html', post_id = post_id)

