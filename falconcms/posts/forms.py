#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""posts/forms.py: Post forms."""

from flask_wtf import Form
from wtforms import TextField, SelectField, TextAreaField, BooleanField,\
    HiddenField
from wtforms.validators import DataRequired


class EditForm(Form):

    """Create edit form for posts."""

    title = TextField(
        'title', validators=[DataRequired()]
    )
    slug = TextField('slug')
    status = SelectField(
        'status', choices=[('1', 'Draft'), ('2', 'Published')]
    )
    change_date = BooleanField('Edit publish date')
    date = TextField('date')
    time = TextField('time')
    content = TextAreaField('content')
    post_id = HiddenField('post_id')
    user_id = HiddenField('user_id', validators=[DataRequired()])
