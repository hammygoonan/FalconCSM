#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for users module."""

from tests.base import BaseTestCase
from flask.ext.login import current_user
from falconcms import bcrypt
from flask import url_for


class UsersTestCase(BaseTestCase):

    """User test cases."""

    def test_login_page(self):
        """Test login page."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_can_login(self):
        """Test user can login."""
        with self.client:
            response = self.login()
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You are now logged in.', response.data)
            self.assertTrue(current_user.is_active())
            self.assertTrue(current_user.email == 'test@example.com')

    def test_cant_login(self):
        """Test that can't login with incorrect details and flash message."""
        with self.client:
            response = self.client.post(
                '/login',
                follow_redirects=True,
                data=dict(
                    email='wrong@email.com',
                    password='password'
                ),
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invalid username or password.', response.data)
            self.assertFalse(current_user.is_active())

    def test_edit_page(self):
        """Test user edit page."""
        with self.client:
            self.login()
            response = self.client.get('/users/edit')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Edit your details', response.data)

    def test_logout(self):
        """Test user can logout."""
        with self.client:
            self.login()
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were logged out', response.data)
            self.assertFalse(current_user.is_active())

    def test_logout_route_requires_login(self):
        """Ensure that logout page requires user to be logged in."""
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please login to view that page.', response.data)

    def test_user_can_change_email(self):
        """Test the user can update email."""
        with self.client:
            self.login()
            self.assertEqual(current_user.email, 'test@example.com')
            # update email
            response = self.client.post(
                '/users/edit',
                data={
                    'email': 'new@example.com',
                    'password': '',
                    'confirm_password': ''
                },
                follow_redirects=True
            )
            # check email has been updated
            self.assertEqual(current_user.email, 'new@example.com')
            # make sure password hasn't been updated
            password = bcrypt.check_password_hash(
                current_user.password, 'password'
            )
            self.assertTrue(password)
            # check flash message
            self.assertIn(b'Your details have been updated', response.data)

    def test_user_can_change_password(self):
        """Test that user can change password."""
        with self.client:
            self.login()
            user_password = bcrypt.check_password_hash(
                current_user.password, 'password'
            )
            self.assertTrue(user_password)
            response = self.client.post(
                '/users/edit',
                data={
                    'email': 'test@example.com',
                    'password': 'new password',
                    'confirm_password': 'new password'
                },
                follow_redirects=True
            )
            # check password is updated
            new_password = bcrypt.check_password_hash(
                current_user.password, 'new password'
            )
            self.assertTrue(new_password)
            # check email remains the same
            self.assertTrue(current_user.email ==
                            'test@example.com')
            # check flash message
            self.assertIn(b'Your details have been updated', response.data)

    def test_user_unique_when_editing(self):
        """Test that email being edited is unique and email is not updated."""
        with self.client:
            self.login()
            self.assertTrue(current_user.email == 'test@example.com')
            response = self.client.post(
                '/users/edit',
                data={
                    'email': 'other@example.com',
                    'password': ''
                },
                follow_redirects=True
            )
            # check email has not been updated
            self.assertTrue(current_user.email ==
                            'test@example.com')
            # display flash message
            self.assertIn(b'That email address is already in use.',
                          response.data)

    def test_user_email_valid_when_editing(self):
        """Test user has entered a valid email address."""
        with self.client:
            self.login()
            # no email address
            response = self.client.post(
                '/users/edit',
                data={
                    'email': '',
                    'password': ''
                },
                follow_redirects=True
            )
            # display flash message
            self.assertIn(b'This field is required.', response.data)
            # invalid email address
            response = self.client.post(
                '/users/edit',
                data={
                    'email': 'not an email',
                    'password': ''
                },
                follow_redirects=True
            )
            # display flash message
            self.assertIn(b'Invalid email address.',
                          response.data)
            # change email but not password
            response = self.client.post(
                '/users/edit',
                data={
                    'email': '',
                    'password': 'new password',
                    'confirm_password': 'new password'
                },
                follow_redirects=True
            )
            # display flash message
            self.assertIn(b'This field is required.',
                          response.data)
