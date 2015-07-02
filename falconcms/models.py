#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""models.py: Website data models."""

from falconcms import db
from falconcms import bcrypt


taxonomy = db.Table(
    'posts_taxonomy',
    db.Column('taxonomy_id', db.Integer, db.ForeignKey('taxonomy.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)

role = db.Table(
    'user_role',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


class Post(db.Model):

    """Post model."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    published = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    post_type = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    author = db.relationship('User')

    taxonomy = db.relationship(
        'Taxonomy', secondary=taxonomy,
        backref=db.backref('posts', lazy='dynamic'))

    STATUS_DRAFT = 1
    STATUS_PUBLISHED = 2
    STATUS_DELETED = 3

    TYPE_POST = 1
    TYPE_PAGE = 2

    def __init__(self, title, content, created, modified, published, status,
                 post_type, author):
        """Initialise model."""
        self.title = title
        self.content = content
        self.created = created
        self.modified = modified
        self.published = published
        self.status = status
        self.post_type = post_type
        self.author = author


class User(db.Model):

    """User model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String)
    handle = db.Column(db.String)

    roles = db.relationship(
        'Role', secondary=role,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, password, name, handle=None):
        """Initialise model."""
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.name = name
        self.handle = handle

    def is_authenticated(self):
        """All users are automatically authenticated."""
        return True

    def is_active(self):
        """All users are automatically active."""
        return True

    def is_anonymous(self):
        """No anonymous users."""
        return False

    def get_id(self):
        """Make sure id returned is unicode."""
        return self.id

    def is_editor(self):
        """Return True is assigned editor role. False otherwise."""
        for role in self.roles:
            if role.role == 'Editor':
                return True
        return False


class Role(db.Model):

    """Role model."""

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer)

    def __init__(self, role):
        """Initialise."""
        self.role = role


class Taxonomy(db.Model):

    """Taxonomy model."""

    __tablename__ = 'taxonomy'
    CATERGORY = 1
    TAG = 2

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    tag_type = db.Column(db.Integer)

    def __init__(self, name, tag_type):
        """Initialise."""
        self.name = name
        self.tag_type = tag_type


class Option(db.Model):

    """Options model."""

    __tablename__ = 'options'

    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.Integer)
    value = db.Column(db.Text)

    def __init__(self, option, value):
        self.option = option
        self.value = value
