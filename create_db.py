#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""create_db.py: Create database and a range of dummy data for testing."""


from falconcms import db
from datetime import datetime, timedelta
from falconcms.models import User, Post, Taxonomy, Role, Option


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
    post = Post('New Post', post_content, None, datetime.now(), datetime.now(),
                datetime.now(), 2, 1, user)
    second_post = Post('The Second Post', 'this is the content for the '
                       'second post', None, datetime.now(), datetime.now(),
                       datetime.now(), 1, 1, user)
    other_post = Post('The Other Second Post', 'this is the content for the '
                      'other post', None, datetime.now(), datetime.now(),
                      datetime.now(), 2, 1, other_user)
    plus_five_hours = datetime.now() + timedelta(hours=5)
    publish_in_future = Post('Future Post', 'This post will be published in'
                             'the future', None, datetime.now(),
                             datetime.now(), plus_five_hours, 2, 1, other_user)
    unpublished = Post('Unpublished', 'This post is still a draft', None,
                       datetime.now(), datetime.now(), datetime.now(), 1, 1,
                       other_user)
    tag = Taxonomy('New Tag', 2)
    category = Taxonomy('New Category', 1)
    editor = User('edit@mypost.com', 'editors password', 'Editor', 'editor')
    editor.roles.append(editor_role)

    # options
    site_name = Option('site_url', 'http://example.com')
    db.session.add_all([
        admin_role,
        editor_role,
        author_role,
        user,
        post,
        second_post,
        publish_in_future,
        unpublished,
        tag,
        category,
        other_user,
        other_post,
        no_post_login,
        editor,
        site_name
    ])
    db.session.commit()
