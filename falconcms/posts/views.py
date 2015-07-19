#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""posts/views.py: Post views."""

from flask import render_template, Blueprint, request, redirect, abort, flash,\
    url_for
from falconcms import db
from datetime import datetime
import re
from falconcms.models import Post
from flask.ext.login import login_required, current_user
from .forms import EditForm

posts_blueprint = Blueprint(
    'posts', __name__,
    template_folder='templates'
)


@posts_blueprint.route('/')
def home():
    """Home page, a list of posts."""
    posts = Post.query.filter(
        Post.published < datetime.now(),
        Post.status == 2
    ).limit(10).all()
    return render_template('index.html', posts=posts)


@posts_blueprint.route('/<path:post_slug>')
def single_post(post_slug):
    """Single post page."""
    post = Post.query.filter(
        Post.slug == post_slug, Post.status == 2
    ).first_or_404()
    return render_template('post.html', post=post)


@posts_blueprint.route('/posts/edit/<int:post_id>', methods=['GET'])
@login_required
def post_edit(post_id=None):
    """Display post edit form."""
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post.author_id != current_user.id and not current_user.is_editor():
        abort(404)
    post.time = post.published.strftime('%H:%M')
    post.date = post.published.strftime('%d-%m-%Y')
    post.post_id = post.id
    post.user_id = current_user.id
    form = EditForm(data=post.__dict__)
    return render_template('edit_post.html', form=form)


@posts_blueprint.route('/posts/save', methods=['POST'])
@login_required
def post_save():
    """Update post."""
    form = EditForm()
    post_id = request.form.get('post_id')
    change_date = request.form.get('change_date')
    published = None
    date = request.form.get('date')
    time = request.form.get('time')
    user_id = request.form.get('user_id')
    if not form.validate_on_submit():
        flash('Some fields were missing.')
        if post_id:
            return redirect('/posts/edit/' + str(post_id))
        else:
            form = EditForm()
            return render_template('edit_post.html', post=None, form=form)

    if current_user.id != int(user_id) or not user_id:
        abort(404)

    if change_date:
        published = validate_published(date, time)
        if not published:
            # if dates are invalid
            flash('The date and/or time fields were not property formatted.')
            if post_id:
                return redirect('/posts/edit/' + str(post_id))
            else:
                form = EditForm()
                return render_template('edit_post.html', post=None, form=form)
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
        post.status = request.form.get('status')
        post.slug = request.form.get('slug')
        if published:
            post.published = published
        message = 'Post updated.'
    # if new
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        slug = request.form.get('slug')
        now = datetime.now()
        if not published:
            published = now
        post = Post(title, content, slug, now, now, published, 1, 1,
                    current_user)
        message = 'Post created.'
    db.session.add(post)
    db.session.commit()
    flash(message)
    return redirect('/posts/edit/' + str(post.id))


def validate_published(date, time):
    """Validate date and time fields."""
    if(
        re.search('[0-9]{2}-[0-9]{2}-[0-9]{4}', date) and
        re.search('[0-9]{2}:[0-9]{2}', time)
    ):
        date = [int(x) for x in date.split('-')]
        time = [int(x) for x in time.split(':')]
        return datetime(date[2], date[1], date[0], time[0], time[1])
    else:
        # if dates are invalid
        False


@posts_blueprint.route('/posts')
@login_required
def post_list():
    """List of posts for users."""
    if current_user.is_editor():
        posts = Post.query.filter(Post.status != 3).all()
    else:
        posts = Post.query.filter(
            Post.author_id == current_user.id,
            Post.status != 3
        ).all()
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
    post.status = 3
    db.session.commit()
    flash('Post deleted.')
    return redirect(url_for('posts.post_list'))
