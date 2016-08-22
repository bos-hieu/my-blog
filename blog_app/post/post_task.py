from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect, flash, \
     jsonify, abort, escape, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from ..post import post
from ..models import Users, Posts, db, Tags, posts_tags, Categories, Comments
from ..decorators import login_required
from ..valids import *


@post.route('/all')
def show_all_posts():
    '''Show all posts of blog'''
    categories = Categories.query.all()
    posts = Posts.query.order_by(Posts.pub_date.desc()).all()
    return render_template("show_all_posts.html",
                           posts = posts,
                           categories=categories)


@post.route('/<int:post_id>')
def show_post(post_id):
    '''Show a post of blog'''
    categories = Categories.query.all()
    post = Posts.query.get(post_id)

    if post:
        return render_template("show_post.html",
                               post = post,
                               categories=categories)
    return "Haven't this post!"


@post.route('/new', methods=['GET','POST'])
@login_required
def new_post():
    '''Create a new post'''
    categories = Categories.query.all()
    tags = Tags.query.all()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_name = request.form.get('category')
        tags_name = request.form.getlist('tags')
        error = "We need both a title and some content!"

        if title and content:
            new_post = Posts(title = title, content = content.replace("\n", "<br>"))
            current_user = Users.query.filter_by(username=session.get('username')).first()
            category = Categories.query.filter_by(name = category_name).first()
            new_post.users = current_user
            new_post.categories = category
            for tag_name in tags_name:
                tag = Tags.query.filter_by(name=tag_name).first()
                new_post.tags.append(tag)
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('post.show_post',
                                    post_id = new_post.id))
        else:
            return render_template('new_post.html',
                                   error = error,
                                   categories = categories,
                                   tags = tags)
    else:
        return render_template('new_post.html',
                               categories = categories,
                               tags = tags)


@post.route('/<int:post_id>/edit', methods=['GET','POST'])
@login_required
def edit_post(post_id):
    ''''edit a post'''
    categories = Categories.query.all()
    tags = Tags.query.all()
    edited_post = Posts.query.get(post_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_name = request.form.get('category')
        tags_name = request.form.getlist('tags')
        error = "We need both a title and some content!"
        if title and content:
            edited_post.title = title
            edited_post.content = content.replace("\n", "<br>")
            edited_post.pub_date = datetime.utcnow()
            category = Categories.query.filter_by(name = category_name).first()
            edited_post.categories = category

            for tag_name in tags_name:
                tag = Tags.query.filter_by(name=tag_name).first()
                if tag not in edited_post.tags:
                    edited_post.tags.append(tag)

            for tag in edited_post.tags:
                if tag.name not in tags_name:
                    edited_post.tags.remove(tag);

            db.session.add(edited_post)
            db.session.commit()
            return redirect(url_for('post.show_post',post_id = edited_post.id))
        else:
            return render_template('edit_post.html', error = error)
    else:
        return render_template('edit_post.html',
                               post = edited_post,
                               categories = categories,
                               tags = tags)


@post.route('/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    """delete a post"""

    if request.method == 'POST':
        #post = Post.query.filter_by(id=post_id).first()
        post = Posts.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('post.show_all_posts'))
    else:
        return render_template('delete_post.html', post_id = post_id)


@post.route('s/tag/<tag_name>')
def show_posts_of_tag(tag_name):
    "Show all post of tag_name"

    tag = Tags.query.filter_by(name = tag_name).first()
    posts = tag.posts

    return render_template("show_all_posts.html",
                           posts = posts,
                           categories = Categories.query.all())


@post.route('s/category/<category_name>')
def show_posts_of_category(category_name):
    "Show all post of category_name"

    category = Categories.query.filter_by(name=category_name).first()
    posts = category.posts

    return render_template("show_all_posts.html",
                           posts = posts,
                           categories = Categories.query.all())


@post.route('/<int:post_id>', methods=('GET','POST'))
@login_required
def new_comment(post_id):
    "Create a new comment in post have post_id"
    if request.method == 'POST':
        comment_content = request.form.get('comment')

        if comment_content:
            post = Posts.query.get(post_id)
            comment = Comments(session.get('username'), comment_content)
            comment.posts = post
            db.session.add(comment)
            db.session.commit()

    return redirect(url_for('post.show_post',post_id = post.id))


@post.route('s/JSON')
def posts_JSON():
    """Return JSON format for all posts"""
    posts = db.session.query(Posts).all()
    return jsonify(posts = [p.serialize for p in posts])


@post.route('/<int:post_id>/JSON')
def post_JSON(post_id):
    """Return JSON format for a post"""
    #post = db.session.query(Post).filter_by(id=post_id).first()
    post = db.session.query(Posts).get(post_id)

    if post:
        return jsonify(post = post.serialize)
    else:
        return "Haven't this post!"
