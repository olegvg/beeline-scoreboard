# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import random
from sqlalchemy import Column, ForeignKey, Integer, UnicodeText, Boolean, Interval
from sqlalchemy.orm import relationship, backref
# import requests

from bl_scoreboard.lib.database import Base


class Score(Base):
    __tablename__ = 'scores'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    # allow cascaded removal of gamer along with its assco'd rows
    gamer_ref = Column(Integer, ForeignKey('gamers.id', ondelete='cascade'), nullable=False, index=True)
    gamer = relationship("Gamer", backref=backref('scores_assoc', cascade='all,delete-orphan'))
    game_name = Column(UnicodeText)
    participate = Column(Integer, default=0)   # 0 - no, 1 - yes
    score = Column(Integer, default=0)
    photos = Column(Integer, default=0)
    most_pins = Column(Integer, default=0)
    best_time = Column(Interval)


class Gamer(Base):
    __tablename__ = 'gamers'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    phone = Column(UnicodeText, unique=True, index=True)
    name = Column(UnicodeText)
    surname = Column(UnicodeText)
    age = Column(UnicodeText)
    promo_code = Column(UnicodeText, unique=True, index=True)
    is_prize_given = Column(Boolean, index=True, default=False)
    # 'scores_assoc' column backref'ed from Gamers_x_Games_Assoc

    def __init__(self, *args, **kwargs):
        promo_code = Gamer.generate_promo_code()
        kwargs['promo_code'] = promo_code
        # params = {
        #     'text': u'Ваш ID {}. Набирайте баллы и получайте призы! Ваш “Билайн”!'.format(promo_code),
        #     'phone': kwargs['phone']
        # }
        # requests.get('https://api.wowcall.ru/p/sms.php', params=params, verify=False)

        super(Gamer, self).__init__(*args, **kwargs)

    @staticmethod
    def generate_promo_code():
        while True:
            rand_candidate = "{:04d}".format(random.randint(99, 9999))
            try_gamer = Gamer.query.filter_by(promo_code=rand_candidate).first()
            if try_gamer is None:
                return rand_candidate

