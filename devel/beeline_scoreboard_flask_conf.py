# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from datetime import timedelta

DEBUG = True

# Timezone definition
LOCAL_TZ = 'Europe/Moscow'

# Session config
SECRET_KEY = 'oZNxrGqqNZULwEB1f6tcZwEmnw721nL8cqqdLDdKPQ0X2YOPLDvsBu4im19IfcBgD2UyZrWdg96UKBNr5VwgwuP+Wf/vFA1Hnohrw4JQ'
PERMANENT_SESSION_LIFETIME = timedelta(days=1)
SESSION_REFRESH_EACH_REQUEST = False
SESSION_COOKIE_NAME = 'bl.scoreboard.session'

SQLALCHEMY_DATABASE_URI = 'postgresql://me_advert:1qazxsw2@int.ovg.me:5432/bl-scoreboard-test'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///../tmp/scoreboard.db'
SQLALCHEMY_SESSION_AUTOCOMMIT = False
SQLALCHEMY_SESSION_AUTOFLUSH = False