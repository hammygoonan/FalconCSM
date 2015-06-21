#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing models."""


from tests.base import BaseTestCase
from falconcms import models, db
from datetime import datetime


class ModelTestCase(BaseTestCase):

    """Model page test."""

    def setUp(self):
        """Setup tests."""
        db.create_all()
        user = models.User('test@example.com', 'password',
                           'John Henry', 'big_j')
        post = models.Post('New Post', 'post content', datetime.now(),
                           datetime.now(), 1, 1, user)
        tag = models.Taxonomy('New Tag', 2)
        category = models.Taxonomy('New Category', 1)
        db.session.add_all([
            models.Role('Administrator'),
            models.Role('Editor'),
            models.Role('Author'),
            user,
            post,
            tag,
            category
        ])
        db.session.commit()

    def test_can_create_user_roles(self):
        """Test it is possible to create a role."""
        roles = models.Role.query.all()
        self.assertTrue(len(roles) == 3)

    def test_can_create_users(self):
        """Test user has been created."""
        user = models.User.query.get(1)
        self.assertEqual('test@example.com', user.email)
        self.assertEqual('John Henry', user.name)
        self.assertEqual('big_j', user.handle)
        self.assertEqual(True, user.is_authenticated())
        self.assertEqual(True, user.is_active())
        self.assertEqual(False, user.is_anonymous())
        # check id is unicode
        user_id = user.get_id()
        self.assertTrue(isinstance(user_id, int))

    def test_can_assign_role(self):
        """Test a user can be assigned a role."""
        role = models.Role.query.get(1)
        user = models.User.query.get(1)
        user.role.append(role)
        db.session.add(user)
        db.session.commit()
        user = models.User.query.get(1)
        self.assertEqual(1, user.role[0].id)

    def test_can_create_posts(self):
        """Test posts are created."""
        post = models.Post.query.get(1)
        self.assertEqual('New Post', post.title)
        self.assertEqual('John Henry', post.author.name)

    def test_can_create_taxonomy(self):
        """Test Taxonomy items are able to be created."""
        category = models.Taxonomy.query.filter_by(tag_type=1).first()
        tag = models.Taxonomy.query.filter_by(tag_type=2).first()
        self.assertEqual('New Category', category.name)
        self.assertEqual(1, category.tag_type)
        self.assertEqual('New Tag', tag.name)
        self.assertEqual(2, tag.tag_type)

    def test_can_link_tags_to_post(self):
        """Test tags and categories can be added to posts."""
        post = models.Post.query.get(1)
        category = models.Taxonomy.query.filter_by(tag_type=1).first()
        tag = models.Taxonomy.query.filter_by(tag_type=2).first()
        post.taxonomy.extend([category, tag])
        db.session.commit()
        post = models.Post.query.get(1)
        self.assertTrue(len(post.taxonomy) == 2)
        for taxonomy in post.taxonomy:
            if taxonomy.tag_type == 1:
                self.assertTrue('New Category', taxonomy.name)
            elif taxonomy.tag_type == 2:
                self.assertTrue('New Tag', taxonomy.name)