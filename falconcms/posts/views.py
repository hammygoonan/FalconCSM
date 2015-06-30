#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""posts/views.py: Post views."""

from flask import render_template, Blueprint, request, redirect, abort, flash
from falconcms import db
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


@posts_blueprint.route('/posts/edit', methods=['POST'])
@login_required
def post_update():
    """Update post."""
    # need to be logged in to edit. XSS protection
    user_id = request.form.get('user_id')
    post_id = request.form.get('post_id')
    if not user_id or not post_id:
        abort(404)
    # bit of an XSS test.
    if current_user.id != int(user_id):
        abort(404)
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    # if current user isn't author, check they are an editor
    if post.author_id != current_user.id and not current_user.is_editor():
        abort(404)
    post.title = request.form.get('title')
    post.content = request.form.get('content')
    db.session.add(post)
    db.session.commit()
    flash('Post updated.')
    return redirect('/posts/edit/' + post_id)


@posts_blueprint.route('/posts/list')
@login_required
def post_list():
    """List of posts for users."""
    posts = Post.query.filter_by(author_id=current_user.id).all()
    return render_template('list.html', posts=posts)


@posts_blueprint.route('/posts/add', methods=['GET', 'POST'])
@login_required
def post_add():
    """Add new post."""
    pass


@posts_blueprint.route('/posts/delete/<int:post_id>')
@login_required
def post_delete(id):
    """Delete Posts."""
    pass
