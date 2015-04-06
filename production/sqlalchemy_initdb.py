# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from bl_scoreboard import model
from bl_scoreboard.model import Base

# SQLA_URL_TEST = 'postgresql://me_advert:1qazxsw2@int.ovg.me:5432/bl-scoreboard-test'
SQLA_URL_TEST = 'sqlite:///../tmp/scoreboard.db'


def init_sqla(sqla_url):

    engine = create_engine(sqla_url, echo=True)
    sqla_session = scoped_session(sessionmaker(autocommit=True,
                                               autoflush=False,
                                               bind=engine))
    Base.query = sqla_session.query_property()

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return sqla_session


def fillup_db(session):
    objects = []

    g = model.Gamer(name=u"Вася", phone='1234567')
    s = model.Score(gamer=g, game_name=u"Танцы", participate=1, score=12)


    session.begin()
    session.add_all([g, s])
    session.commit()


if __name__ == '__main__':
    print "init"
    session = init_sqla(SQLA_URL_TEST)
    # fillup_db(session)