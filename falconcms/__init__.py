#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main app entry point."""

import os
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


@app.route("/")
def hello():
    """Hello world."""
    return render_template('base.html')

if __name__ == "__main__":
    app.run()
