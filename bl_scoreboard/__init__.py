# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import os
import logging

from flask import Flask, send_from_directory
from sqlalchemy import create_engine

from lib.database import Base
from lib.database import sqla_session
from rest import init_blueprint as init_rest_blueprint


app = Flask('bl_scoreboard')
app.config.from_object('beeline_scoreboard_flask_conf')

# Init blueprints
init_rest_blueprint(app)

# Add engine to SQLAlchemy session
sqlserver_uri = app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(sqlserver_uri)
sqla_session.configure(bind=engine)

if app.debug:
    sqla_logger = logging.getLogger('sqlalchemy')
    sqla_logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    sqla_logger.addHandler(stream_handler)

    # Disable caching of HTTP responses in debug mode. It's critical for debugging frontend / js code
    @app.after_request
    def no_cache(response):
        response.headers['Cache-Control'] = 'no-cache, no-store'
        response.headers['Pragma'] = 'no-cache'
        return response

    # Gain access to ./dist directory as http://site/dist to debug production environment
    @app.route('/dist/<path:filename>')
    def static_dist(filename):
        path = os.path.dirname(__file__)
        path = os.path.join(path, './dist')
        return send_from_directory(path, filename)

else:
    app.logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(module)s.%(funcName)s - %(message)s')
    stream_handler.setFormatter(formatter)
    app.logger.addHandler(stream_handler)

# See http://flask.pocoo.org/docs/patterns/sqlalchemy/
@app.teardown_request
def shutdown_session(exception=None):
    sqla_session.remove()