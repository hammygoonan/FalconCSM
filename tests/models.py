#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing models."""


from tests.base import BaseTestCase
from falconcms import models, db


class ModelTestCase(BaseTestCase):

    """Model page test."""

    def test_can_create_user_roles(self):
        """Test it is possible to create a role."""
        roles = models.Role.query.all()
        self.assertTrue(len(roles) == 3)

    def test_can_create_users(self):
        """Test user has been created."""
        user = models.User.query.get(2)
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
        user = models.User.query.get(2)
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        user = models.User.query.get(2)
        self.assertEqual(1, user.roles[0].id)

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

    def test_can_get_option(self):
        """Can read Options."""
        option = models.Option.query.get(1)
        self.assertEqual('site_url', option.option)
        self.assertEqual('http://example.com', option.value)

    def test_can_save_option(self):
        """New Options can be saved."""
        db.session.add(models.Option('new option', 'new value'))
        db.session.commit()
        option = models.Option.query.filter_by(value='new value').first()
        self.assertEqual('new value', option.value)

    def test_can_update_option(self):
        """Options can be updated."""
        option = models.Option.query.get(1)
        option.value = 'http://httpbin.org'
        db.session.commit()
        option = models.Option.query.get(1)
        self.assertEqual('http://httpbin.org', option.value)
