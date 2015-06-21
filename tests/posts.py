#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing post pages."""


from tests.base import BaseTestCase


class PostsTestCase(BaseTestCase):

    """Post page test."""

    # def test_post_edit_page(self):
    #     """Test post edit page to ensure it displays correctly."""
    #     response = self.client.get(
    #         '/', content_type='html/text',
    #         follow_redirects=True
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Create New Post', response.data)
