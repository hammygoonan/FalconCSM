#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""posts/views.py: Post views."""

from flask import render_template, Blueprint
from falconcms.models import Post
from flask.ext.login import login_required, current_user

posts_blueprint = Blueprint(
    'posts', __name__,
    template_folder='templates'
)


@posts_blueprint.route('/')
def home():
    """Home page, a list of posts."""
    posts = Post.query.all().limit(10)
    return render_template('index.html', posts=posts)


@posts_blueprint.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_edit(id):
    """Edit post."""
    pass


@posts_blueprint.route('/posts/list')
@login_required
def post_list(id):
    """List of posts for users."""
    posts = Post.query.filter_by(author_id=current_user.id).all()
    return render_template('index.html', posts=posts)


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
