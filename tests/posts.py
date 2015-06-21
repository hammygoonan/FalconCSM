#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing post pages."""


from tests.base import BaseTestCase


class PostsTestCase(BaseTestCase):

    """Post page test."""

    def test_home_page(self):
        """Test home page to make sure it displays a list of posts."""
        response = self.client.get(
            '/', content_type='html/text',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h2>First Post Header</h2>', response.data)
        self.assertIn(b'<li>first item</li>', response.data)
        self.assertIn(b'<a href="http://httpbin.com">a link</a>',
                      response.data)
