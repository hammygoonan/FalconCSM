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

    def test_post_edit_page_with_author(self):
        """Test Author functionality when editing posts."""
        with self.client:
            self.login()
            response = self.client.get(
                '/posts/edit/1', content_type='html/text',
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'New Post', response.data)
        with self.client:
            self.other_login()
            response = self.client.get(
                '/posts/edit/1', content_type='html/text',
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 404)
        with self.client:
            self.login()
            response = self.client.get(
                '/posts/edit/999999', content_type='html/text',
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 404)
        with self.client:
            self.login()
            self.client.post(
                '/posts/edit/1', content_type='html/text',
                follow_redirects=True,
                data={
                    'title': 'New Post',
                    'content': 'New content'
                }
            )
            post = Post.query.get(1)
            self.assertNotEqual(post.create, post.modified)
            self.assertEqual('New content', post.content)

    def test_post_edit_page_with_editor(self):
        """Test Editor functionality when editing posts."""
        # TODO check editor can edit
        pass

    def test_post_updated(self):
        pass

    def test_post_list_page(self):
        """Test page displays a list of posts."""
        with self.client:
            response = self.login()
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<td>New Post</td>', response.data)
        with self.client:
            response = self.other_login()
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<td>The Other Second Post</td>', response.data)
            self.assertNotIn(b'<td>New Post</td>', response.data)
        with self.client:
            response = self.no_post_login()
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You don\'t seem to have any posts.', response.data)
            self.assertNotIn(b'<td>New Post</td>', response.data)

    def test_post_add_page(self):
        pass

    def test_post_delete(self):
        pass
