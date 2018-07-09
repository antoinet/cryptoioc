#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cryptoioc:password1@localhost/cryptoioc'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
migrate = Migrate(app, db)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass


from app import models
from app import views
