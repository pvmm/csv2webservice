# -*- coding: utf-8 -*-

import routes, click

from os import environ, path
from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_compress import Compress
from flask_cors import CORS
from environment import static_folder, db_uri, app_base
from psycopg2 import connect
from pprint import pprint


def create_app(app_dir, session=None, db_uri2=None):
    app = Flask('csvserver', static_folder=static_folder)
    app.config.from_pyfile(path.join(app_dir, 'config/app.cfg'))
    #app.config['MONGO_URI'] = db_uri2 or db_uri
    #app.mongo = PyMongo(app, uri=db_uri2)
    #app.mongo.init_app(app=app)
    app.base_dir = app_base
    CORS(app)
    Compress(app)

    app.logger.debug(' * App created.')

    # Define endpoints
    api = Api(app, prefix=app.config['API_PREFIX'])
    routes.add_endpoint(api)
    app.logger.debug(' * API created.')

    return app
