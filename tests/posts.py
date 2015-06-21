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

    def test_post_edit_page(self):
        pass

    def test_post_updated(self):
        pass

    def test_post_list_page(self):
        """Test page displays a list of posts."""
        response = self.client.get(
            '/posts/list', content_type='html/text',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'First Post Header', response.data)
        # TODO check it's only posts from logged in user

    def test_post_add_page(self):
        pass

    def test_post_delete(self):
        pass
