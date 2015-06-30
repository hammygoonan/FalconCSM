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
    admin_role = Role('Administrator')
    editor_role = Role('Editor')
    author_role = Role('Author')
    user = User('test@example.com', 'password', 'John Henry', 'big_j')
    other_user = User('other@example.com', 'other password', 'Major Luddite',
                      'luddites')
    no_post_login = User('nopost@magoo.com', 'magoo password', 'Mr Magoo',
                         'magoo')
    post = Post('New Post', post_content, datetime.now(), datetime.now(), 1,
                1, user)
    second_post = Post('The Second Post', 'this is the content for the '
                       'second post', datetime.now(),
                       datetime.now(), 1, 1, user)
    other_post = Post('The Other Second Post', 'this is the content for the '
                      'second post', datetime.now(),
                      datetime.now(), 1, 1, other_user)
    tag = Taxonomy('New Tag', 2)
    category = Taxonomy('New Category', 1)
    editor = User('edit@mypost.com', 'editors password', 'Editor', 'editor')
    editor.roles.append(editor_role)
    db.session.add_all([
        admin_role,
        editor_role,
        author_role,
        user,
        post,
        second_post,
        tag,
        category,
        other_user,
        other_post,
        no_post_login,
        editor
    ])
    db.session.commit()
