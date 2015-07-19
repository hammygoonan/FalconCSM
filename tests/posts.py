#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing post pages."""


from tests.base import BaseTestCase
from falconcms.models import Post


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
        self.assertNotIn(b'<h1>Future Post</h1>', response.data)
        self.assertNotIn(b'<h1>Unpublished</h1>', response.data)

    def test_single_post(self):
        """Test posts are displayed on single post page."""
        response = self.client.get(
            '/new-post', content_type='html/text',
            follow_redirects=True
        )
        self.assertIn(b'<h1>New Post</h1>', response.data)

    def test_404_if_no_single_post(self):
        """Test 404 page displayed if slug is wrong."""
        response = self.client.get(
            '/this-slug-is-wrong', content_type='html/text',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 404)

    def test_redirect_to_login_in_not_logged_in_on_post_edit_page(self):
        """Check that users are redirect to login page if not logged in."""
        with self.client:
            response = self.client.get(
                '/posts/edit/1', content_type='html/text',
                follow_redirects=True
            )
            self.assertIn(b'Please login to view that page.', response.data)

    def test_200_response_if_logged_in_and_correct_user(self):
        """Check page accessable by logged in user and author/editor."""
        with self.client:
            self.login()
            response = self.client.get(
                '/posts/edit/1', content_type='html/text',
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'New Post', response.data)

    def test_400_response_if_logged_in_and_incorrect_user(self):
        """Test user without permission can't edit page."""
        with self.client:
            self.other_login()
            response = self.client.get(
                '/posts/edit/1', content_type='html/text',
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 404)

    def text_400_if_post_doesnt_exist(self):
        """Test that a 404 is thrown if no post with that id."""
        with self.client:
            self.login()
            response = self.client.get(
                '/posts/edit/999999', content_type='html/text',
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 404)

    def test_post_can_be_updated(self):
        """Test post is updated when edited by valid user."""
        with self.client:
            self.login()
            response = self.client.post(
                '/posts/save',
                follow_redirects=True,
                data={
                    'post_id': 1,
                    'user_id': 2,
                    'status': 2,
                    'title': 'New Post',
                    'content': 'New content'
                }
            )
            post = Post.query.get(1)
            self.assertEqual(response.status_code, 200)
            # dates should have changed. Assume more than a microsecond has
            # passed
            self.assertNotEqual(post.created, post.modified)
            self.assertIn(b'Post updated.', response.data)
            self.assertEqual('New content', post.content)

    def test_post_edit_page_with_editor(self):
        """Test Editor functionality when editing posts."""
        with self.client:
            self.editor_login()
            response = self.client.post(
                '/posts/save',
                follow_redirects=True,
                data={
                    'post_id': 1,
                    'user_id': 1,
                    'status': 1,
                    'title': 'New content',
                    'content': 'An editor edited my content'
                }
            )
            post = Post.query.get(1)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Post updated.', response.data)
            self.assertEqual('New content', post.title)

    def test_editor_gets_full_list(self):
        """Test list page displays full list of posts for editors."""
        response = self.editor_login()
        self.assertIn(b'<td>New Post</td>', response.data)
        self.assertIn(b'<td>The Second Post</td>', response.data)
        self.assertIn(b'<td>The Other Second Post</td>', response.data)

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
        """Test new post can be created."""
        with self.client:
            self.login()
            response = self.client.post(
                '/posts/save',
                follow_redirects=True,
                data={
                    'user_id': 2,
                    'status': 2,
                    'title': 'Added title',
                    'content': 'This is the content of an added post'
                }
            )
        self.assertEqual(response.status_code, 200)
        posts = Post.query.all()
        self.assertEqual('Added title', posts[-1].title)
        self.assertEqual('This is the content of an added post',
                         posts[-1].content)
        self.assertEqual(posts[-1].created, posts[-1].modified)

    def test_required_fields(self):
        """New post should not be created without title."""
        with self.client:
            self.login()
            response = self.client.post(
                '/posts/save',
                follow_redirects=True,
                data={
                    'user_id': 2,
                    'status': 2,
                    'content': 'This is the content of an added post'
                }
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Some fields were missing.', response.data)
        posts = Post.query.filter_by(content='This is the content of an'
                                     'added post').first()
        self.assertFalse(posts)

    def test_cant_create_post_for_another_user(self):
        """Test that a 404 is thrown if wrong user tries to create post."""
        with self.client:
            self.login()
            response = self.client.post(
                '/posts/save',
                follow_redirects=True,
                data={
                    'user_id': 1,
                    'status': 2,
                    'title': 'New content',
                    'content': 'An editor edited my content'
                }
            )
            self.assertEqual(response.status_code, 404)

    def test_post_delete(self):
        """Test post can be deleted."""
        with self.client:
            self.login()
            response = self.client.get(
                'posts/delete/2',
                follow_redirects=True
            )
            self.assertIn(b'Post deleted.', response.data)
            post = Post.query.get(2)
            self.assertEqual(3, post.status)

    def test_wong_user_cant_delete(self):
        """Check that an unauthorised user can't delete."""
        with self.client:
            self.other_login()
            response = self.client.get(
                'posts/delete/2',
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 404)

    def test_editor_can_delete(self):
        """Test post can be deleted by an editor."""
        with self.client:
            self.login()
            response = self.client.get(
                'posts/delete/2',
                follow_redirects=True
            )
            self.assertIn(b'Post deleted.', response.data)
            post = Post.query.get(2)
            self.assertEqual(3, post.status)

    def test_deleted_posts_dont_appear_on_list_page(self):
        """Test deleted posts aren't showing up anywhere."""
        with self.client:
            self.login()
            self.client.get(
                'posts/delete/2',
                follow_redirects=True
            )
            response = self.client.get(
                'posts'
            )
            self.assertNotIn(b'The Second Post', response.data)

    def test_date_published(self):
        """Test published data works."""
        with self.client:
            self.login()
            response = self.client.post(
                '/posts/save',
                follow_redirects=True,
                data={
                    'user_id': 2,
                    'post_id': 2,
                    'status': 2,
                    'change_date': 'yes',
                    'date': '10-12-2016',
                    'time': '12:58',
                    'title': 'Added title',
                    'content': 'This is the content of an added post'
                }
            )
            self.assertIn(b'Post updated.', response.data)
            post = Post.query.get(2)
            self.assertEqual('2016', post.published.strftime('%Y'))

    def test_date_published_doesnt_change(self):
        """Test published date doesn't change if checkbox isn't clicked."""
        with self.client:
            self.login()
            response = self.client.post(
                '/posts/save',
                follow_redirects=True,
                data={
                    'user_id': 2,
                    'post_id': 2,
                    'status': 2,
                    'date': '10-12-2016',
                    'time': '12:58',
                    'title': 'Added title',
                    'content': 'This is the content of an added post'
                }
            )
            self.assertIn(b'Post updated.', response.data)
            post = Post.query.get(2)
            self.assertNotEqual('2016', post.published.strftime('%Y'))

    def test_error_if_published_date_format_incorrect(self):
        """Test published date doesn't change if date format is incorrect."""
        with self.client:
            self.login()
            response = self.client.post(
                '/posts/save',
                follow_redirects=True,
                data={
                    'user_id': 2,
                    'post_id': 2,
                    'status': 2,
                    'change_date': 'yes',
                    'date': '10/12/2016',
                    'time': '12:58',
                    'title': 'Added title',
                    'content': 'This is the content of an added post'
                }
            )
            self.assertIn(b'The date and/or time fields were not property'
                          b' formatted', response.data)
            post = Post.query.get(2)
            self.assertNotEqual('2016', post.published.strftime('%Y'))
