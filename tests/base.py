#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base testing module that other tests extend from."""


from flask.ext.testing import TestCase
from flask import url_for
from falconcms import app, db
from create_db import create_db


class BaseTestCase(TestCase):

    """A base test case."""

    def create_app(self):
        """Create app for tests."""
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        """Setup tests."""
        create_db()

    def tearDown(self):
        """Tear down tests."""
        db.session.remove()
        db.drop_all()

    def login(self):
        """Login to site."""
        return self.client.post(
            url_for('users.login'),
            follow_redirects=True,
            data={
                'email': 'test@example.com',
                'password': 'password'
            },
        )

    def other_login(self):
        """Login to site."""
        return self.client.post(
            url_for('users.login'),
            follow_redirects=True,
            data={
                'email': 'other@example.com',
                'password': 'other password'
            },
        )

    def no_post_login(self):
        """Login to site."""
        return self.client.post(
            url_for('users.login'),
            follow_redirects=True,
            data={
                'email': 'nopost@magoo.com',
                'password': 'magoo password'
            },
        )

    def editor_login(self):
        """Login to site as Editor."""
        return self.client.post(
            url_for('users.login'),
            follow_redirects=True,
            data={
                'email': 'edit@mypost.com',
                'password': 'editors password'
            },
        )
