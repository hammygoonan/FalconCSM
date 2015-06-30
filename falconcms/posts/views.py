#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""posts/views.py: Post views."""

from flask import render_template, Blueprint, request, redirect, abort, flash,\
    url_for
from falconcms import db
from datetime import datetime
from falconcms.models import Post
from flask.ext.login import login_required, current_user

posts_blueprint = Blueprint(
    'posts', __name__,
    template_folder='templates'
)


@posts_blueprint.route('/')
def home():
    """Home page, a list of posts."""
    posts = Post.query.limit(10).all()
    return render_template('index.html', posts=posts)


@posts_blueprint.route('/posts/edit/<int:post_id>', methods=['GET'])
@login_required
def post_edit(post_id=None):
    """Display post edit form."""
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post.author_id != current_user.id and not current_user.is_editor():
        abort(404)
    return render_template('edit_post.html', post=post)


@posts_blueprint.route('/posts/save', methods=['POST'])
@login_required
def post_save():
    """Update post."""
    user_id = request.form.get('user_id')
    if current_user.id != int(user_id) or not user_id:
        abort(404)

    post_id = request.form.get('post_id')
    # if it's an update
    if post_id:
        post = Post.query.get(post_id)
        if not post:
            abort(404)
        # if current user isn't author, check they are an editor
        if post.author_id != current_user.id and not current_user.is_editor():
            abort(404)
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.modified = datetime.now()
        message = 'Post updated.'
    # if new
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        now = datetime.now()
        post = Post(title, content, now, now, 1, 1, current_user)
        message = 'Post created.'
    db.session.add(post)
    db.session.commit()
    flash(message)
    return redirect('/posts/edit/' + str(post.id))


@posts_blueprint.route('/posts')
@login_required
def post_list():
    """List of posts for users."""
    if current_user.is_editor():
        posts = Post.query.all()
    else:
        posts = Post.query.filter_by(author_id=current_user.id).all()
    return render_template('list.html', posts=posts)


@posts_blueprint.route('/posts/add')
@login_required
def post_add():
    """Render new post page."""
    return render_template('edit_post.html', post=None)


@posts_blueprint.route('/posts/delete/<int:post_id>')
@login_required
def post_delete(post_id):
    """Delete Posts."""
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post.author_id != current_user.id and not current_user.is_editor():
        abort(404)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.')
    return redirect(url_for('posts.post_list'))
