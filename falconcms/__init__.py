#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main app entry point."""

import os
import re
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


# Helpers
def is_email(email):
    """Validate that an email is syntactially correct."""
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True

from falconcms.users.views import users_blueprint
app.register_blueprint(users_blueprint)

from falconcms.models import User
login_manager.login_view = "users.login"
login_manager.login_message = "Please login to view that page."


@login_manager.user_loader
def load_user(user_id):
    """Load the logged in user for the LoginManager."""
    return User.query.filter(User.id == int(user_id)).first()


@app.route("/")
def hello():
    """Hello world."""
    return render_template('home.html')

if __name__ == "__main__":
    app.run()
