from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect, flash, \
     jsonify, abort, escape, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from ..post import post
from ..models import Users, Posts, db, Tags, posts_tags, Catalogues, Comments
from ..decorators import login_required
from ..valids import *


@post.route('/all')
def show_all_posts():
    '''Show all posts of blog'''
    catalogues = Catalogues.query.all()
    posts = Posts.query.order_by(Posts.pub_date.desc()).all()
    return render_template("show_all_posts.html",
                           posts = posts,
                           catalogues=catalogues)


@post.route('/<int:post_id>')
def show_post(post_id):
    '''Show a post of blog'''
    catalogues = Catalogues.query.all()
    post = Posts.query.get(post_id)

    if post:
        return render_template("show_post.html",
                               post = post,
                               catalogues=catalogues)
    return "Haven't this post!"


@post.route('/new', methods=['GET','POST'])
@login_required
def new_post():
    '''Create a new post'''
    catalogues = Catalogues.query.all()
    tags = Tags.query.all()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        catalogue_name = request.form.get('catalogue')
        tags_name = request.form.getlist('tags')
        error = "We need both a title and some content!"

        if title and content:
            new_post = Posts(title = title, content = content.replace("\n", "<br>"))
            current_user = Users.query.filter_by(username=session.get('username')).first()
            catalogue = Catalogues.query.filter_by(name = catalogue_name).first()
            new_post.users = current_user
            new_post.cataloges = catalogue
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
                                   catalogues = catalogues,
                                   tags = tags)
    else:
        return render_template('new_post.html',
                               catalogues = catalogues,
                               tags = tags)


@post.route('/<int:post_id>/edit', methods=['GET','POST'])
@login_required
def edit_post(post_id):
    ''''edit a post'''
    edited_post = Posts.query.get(post_id)

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
                           catalogues = Catalogues.query.all())


@post.route('s/catalogue/<catalogue_name>')
def show_posts_of_catalogue(catalogue_name):
    "Show all post of catalogue_name"

    catalogue = Catalogues.query.filter_by(name=catalogue_name).first()
    catalogues = Catalogues.query.all()
    posts = catalogue.posts

    return render_template("show_all_posts.html",
                           posts = posts,
                           catalogues = Catalogues.query.all())


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
