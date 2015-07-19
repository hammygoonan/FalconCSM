#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""users/forms.py: Post forms."""

from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):

    """Login form."""

    email = TextField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class EditUserForm(Form):

    """Edit user form."""

    email = TextField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password')
