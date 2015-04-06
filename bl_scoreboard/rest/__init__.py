# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from gamers import gamers_bp


def init_blueprint(app):
    app.register_blueprint(gamers_bp, url_prefix='/gamers')