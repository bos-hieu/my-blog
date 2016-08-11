from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect, flash, \
     jsonify, abort, escape, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from ..post import post
from ..models import User, Post, db
from ..decorators import login_required
from ..valids import *


@post.route('/all')
def show_all_posts():
    ''''Show all posts of blog'''
    posts = Post.query.order_by(Post.pub_date.desc()).all()
    return render_template("show_all_posts.html", posts = posts)


@post.route('/<int:post_id>')
def show_post(post_id):
    """Show a post of blog"""
    post = Post.query.filter_by(id=post_id).first()

    if post:
        return render_template("show_post.html", post = post)
    return "Haven't this post!"


@post.route('/new', methods=['GET','POST'])
@login_required
def new_post():
    ''''Create a new post'''
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error = "We need both a title and some content!"

        if title and content:
            new_post = Post(title = title, content = content.replace("\n", "<br>"))
            current_user = User.query.filter_by(username=session.get('username')).one()
            new_post.user = current_user
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('post.show_post',post_id = new_post.id))
        else:
            return render_template('new_post.html', error = error)
    else:
        return render_template('new_post.html')


@post.route('/<int:post_id>/edit', methods=['GET','POST'])
@login_required
def edit_post(post_id):
    ''''edit a post'''
    edited_post = Post.query.filter_by(id=post_id).first()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error = "We need both a title and some content!"
        if title and content:
            edited_post.title = title
            edited_post.content = content.replace("\n", "<br>")
            edited_post.pub_date = datetime.utcnow()
            db.session.add(edited_post)
            db.session.commit()
            return redirect(url_for('post.show_post',post_id = edited_post.id))
        else:
            return render_template('edit_post.html', error = error)
    else:
        return render_template('edit_post.html',
                               post_id = post_id,
                               post = edited_post)


@post.route('/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    """delete a post"""
    
    if request.method == 'POST':
        post = Post.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('post.show_all_posts'))
    else:
        return render_template('delete_post.html', post_id = post_id)


@post.route('s/JSON')
def posts_JSON():
    """Return JSON format for all posts"""
    posts = db.session.query(Post).all()
    return jsonify(posts = [p.serialize for p in posts])


@post.route('/<int:post_id>/JSON')
def post_JSON(post_id):
    """Return JSON format for a post"""
    post = db.session.query(Post).filter_by(id=post_id).first()
    
    if post:
        return jsonify(post = post.serialize)
    else:
        return "Haven't this post!"
