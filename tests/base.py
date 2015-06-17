#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base testing module that other tests extend from."""


from flask.ext.testing import TestCase
from falconcms import app


class BaseTestCase(TestCase):

    """A base test case."""

    def create_app(self):
        """Create app for tests."""
        return app

    def setUp(self):
        """Setup tests."""
        pass

    def tearDown(self):
        """Tear down tests."""
        pass
