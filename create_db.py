#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""create_db.py: Create database and a range of dummy data for testing."""


from falconcms import db
from datetime import datetime
from falconcms.models import User, Post, Taxonomy, Role


post_content = """##First Post Header

* first item
* second item
[a link](http://httpbin.com)
"""


def create_db():
    """Create database for tests."""
    db.create_all()
    user = User('test@example.com', 'password',
                'John Henry', 'big_j')
    other_user = User('other@example.com', 'other password', 'Major Luddite',
                      'luddites')
    no_post_user = User('nopost@magoo.com', 'magoo password', 'Nopost Magoo',
                        'magoose')
    post = Post('New Post', post_content, datetime.now(), datetime.now(), 1,
                1, user)
    second_post = Post('The Second Post', 'this is the content for the '
                       'second post', datetime.now(), datetime.now(), 1, 1,
                       user)
    other_user_post = Post('The Other Second Post', 'this is the content for the '
                           'second post', datetime.now(), datetime.now(), 1, 1,
                           other_user)
    tag = Taxonomy('New Tag', 2)
    category = Taxonomy('New Category', 1)
    db.session.add_all([
        Role('Administrator'),
        Role('Editor'),
        Role('Author'),
        user,
        post,
        second_post,
        other_user_post,
        tag,
        category,
        other_user,
        no_post_user
    ])
    db.session.commit()
