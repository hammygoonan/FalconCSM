#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""users/views.py: User views."""

from flask import render_template, Blueprint, request, flash, redirect,\
    url_for
from flask.ext.login import login_user, login_required, logout_user,\
    current_user
from falconcms import db, bcrypt, is_email
from falconcms.models import User

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Login route."""
    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None and bcrypt.check_password_hash(
            user.password, request.form['password']
        ):
            login_user(user)
            # TODO: proper redirect to admin panel
            flash("You are now logged in.")
            return redirect('/')

        else:
            flash('Invalid username or password.')

    return render_template('login.html')


@users_blueprint.route('/logout')
@login_required
def logout():
    """Logout route."""
    logout_user()
    flash('You were logged out')
    # TODO: add proper logout redirect
    flash('You were logged out')
    return redirect('/')


@users_blueprint.route('/users/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Edit user route."""
    if request.method == "POST":
        email = request.form.get('email')
        if not email or not is_email(email):
            flash('Please enter a valid email address.')
            return render_template('edit.html', user=current_user)
        user = User.query.filter_by(email=email).first()
        # if email is already taken
        if user and user.id != current_user.id:
            flash('That email address is already in use.')
        else:
            user = User.query.get(current_user.id)
            # update password if changed
            if request.form['password'] != '':
                user.password = bcrypt.generate_password_hash(
                    request.form['password']
                )
            # update email if changed
            if current_user.email != request.form['email']:
                user.email = request.form['email']
            db.session.commit()
            flash('Your details have been updated')
    return render_template('edit.html', user=current_user)
