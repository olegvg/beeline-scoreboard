# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

SECRET_KEY = '5FcoGoFsj00DFAFQzqCmOkPaVzD1rkNODZnqjkHKscVivV/6XXAsYDvNDkrVykOCApNNrV7+mkUD9kHR4k0pQ+QMoZIEoo0eN4FvEaOO3'
# CSRF_ENABLED = True
SESSION_REFRESH_EACH_REQUEST = False
SESSION_COOKIE_NAME = 'beeline.scoreboard.session'

# SQLALCHEMY_DATABASE_URI = 'postgresql://me_advert:eZdVgekAH_5r@10.49.7.2:5432/bl-scoreboard?sslmode=disable'
SQLALCHEMY_DATABASE_URI = 'sqlite:///../tmp/scoreboard.db'
SQLALCHEMY_SESSION_AUTOCOMMIT = False
SQLALCHEMY_SESSION_AUTOFLUSH = False