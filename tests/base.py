#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base testing module that other tests extend from."""


from flask.ext.testing import TestCase
from falconcms import app, db
from falconcms.models import User, Post, Role, Taxonomy
from datetime import datetime


class BaseTestCase(TestCase):

    """A base test case."""

    def create_app(self):
        """Create app for tests."""
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        """Setup tests."""
        db.create_all()
        user = User('test@example.com', 'password',
                    'John Henry', 'big_j')
        other_user = User('other@example.com', 'other password',
                          'Major Luddite', 'luddites')
        post = Post('New Post', 'post content', datetime.now(),
                    datetime.now(), 1, 1, user)
        tag = Taxonomy('New Tag', 2)
        category = Taxonomy('New Category', 1)
        db.session.add_all([
            Role('Administrator'),
            Role('Editor'),
            Role('Author'),
            user,
            post,
            tag,
            category,
            other_user
        ])
        db.session.commit()

    def tearDown(self):
        """Tear down tests."""
        db.session.remove()
        db.drop_all()
