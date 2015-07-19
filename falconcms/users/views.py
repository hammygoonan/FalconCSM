#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""users/views.py: User views."""

from flask import render_template, Blueprint, request, flash, redirect,\
    url_for
from flask.ext.login import login_user, login_required, logout_user,\
    current_user
from falconcms import db, bcrypt, is_email
from falconcms.models import User
from .forms import LoginForm, EditUserForm

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Login route."""
    form = LoginForm()
    if request.method == "GET":
        return render_template('login.html', form=form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None and bcrypt.check_password_hash(
            user.password, request.form['password']
        ):
            login_user(user)
            flash("You are now logged in.")
            return redirect(url_for('posts.post_list'))
        else:
            flash('Invalid username or password.')
    else:
        flash('Invalid form data.')
    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    """Logout route."""
    logout_user()
    flash('You were logged out')
    return redirect('/')


@users_blueprint.route('/users/edit', methods=['GET', 'POST'])
@login_required
def edit_user():
    """Edit user route."""
    form = EditUserForm(data=current_user.__dict__)
    if request.method == "GET":
        return render_template('edit_user.html', form=form)

    if form.validate_on_submit():
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        # if email is already taken
        if user and user.id != current_user.id:
            flash('That email address is already in use.')
        else:
            user = User.query.get(current_user.id)
            # update password if changed
            if request.form['password'] != '':
                if(
                    request.form['password'] !=
                    request.form['confirm_password']
                ):
                    flash('Passwords did not match.')
                else:
                    user.password = bcrypt.generate_password_hash(
                        request.form['password']
                    )
            # update email if changed
            if current_user.email != request.form['email']:
                user.email = request.form['email']
            db.session.commit()
            flash('Your details have been updated')
    else:
        flash('Your details have not been updated. There were errors in the '
              'form')
    return render_template('edit_user.html', form=form)
