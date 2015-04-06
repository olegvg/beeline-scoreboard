# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from datetime import timedelta
import re
from flask import Blueprint
from flask.ext.restful import reqparse, Resource
from ..lib.rest import Api
from ..lib.utils import str_to_timedelta, timedelta_to_str
from ..model.gamers import Gamer, Score
from ..lib.database import sqla_session
from sqlalchemy import not_, func, desc
from sqlalchemy.orm.exc import NoResultFound
from ..lib.database import compile_query


gamers_bp = Blueprint('gamers', __name__)
endpoint = Api(gamers_bp, catch_all_404s=True)

set_of_games = {"Автогонки", "Танцы", "Пинг-понг", "Велосипед", "I love 4G", "Автосимулятор"}


class SearchByPromoCode(Resource):
    def get(self):
        rp = reqparse.RequestParser()
        rp.add_argument('query', type=unicode, required=True)
        args = rp.parse_args()

        like_arg = u"%{}%".format(args.query)
        gamers = Gamer.query.filter(Gamer.phone.ilike(like_arg)).all()

        return [x.phone for x in gamers]


class MangleGamer(Resource):
    def post(self):
        """
        Creates a new gamer
        """
        rp = reqparse.RequestParser()
        rp.add_argument('name', type=unicode, required=True)
        rp.add_argument('surname', type=unicode, required=True)
        # rp.add_argument('age', type=unicode, required=True)
        rp.add_argument('phone', type=unicode, required=True)
        args = rp.parse_args()

        check_exist = Gamer.query.filter_by(phone=args.phone).first()
        if check_exist is not None:
            return {'status': 'already registered'}, 409

        # gamer = Gamer(phone=args.phone,
        #               name=args.name,
        #               surname=args.surname,
        #               age=args.age)
        gamer = Gamer(phone=args.phone,
                      name=args.name,
                      surname=args.surname)
        sqla_session.add(gamer)
        sqla_session.commit()
        return {'promo_code': gamer.promo_code}

    def put(self):
        """
        Updates existing gamer's score, and data except phone number
        """
        rp = reqparse.RequestParser()
        rp.add_argument('promo_code', type=unicode, required=True)
        rp.add_argument('game_name', type=unicode)
        rp.add_argument('participate', type=int)
        rp.add_argument('score', type=int)
        rp.add_argument('photos', type=int)
        rp.add_argument('most_pins', type=unicode)
        rp.add_argument('best_time', type=unicode)
        rp.add_argument('prize_given', type=bool)
        args = rp.parse_args()

        try:
            gamer = Gamer.query.filter_by(promo_code=args.promo_code).one()
        except NoResultFound:
            return {'status': 'not found'}, 404

        if args.game_name is None:
            gamer.is_prize_given = args.prize_given
            sqla_session.commit()
            return
        try:
            score = Score.query \
                .join(Score.gamer) \
                .filter(Score.game_name == args.game_name,
                        Gamer.promo_code == args.promo_code) \
                .one()

        except NoResultFound:
            score = Score(gamer=gamer, game_name=args.game_name)
            sqla_session.add(score)
        if args.participate:
            score.participate = args.participate
        if args.score:
            score.score = args.score
        if args.photos:
            score.photos = args.photos
        if args.most_pins:
            try:
                score.most_pins = int(args.most_pins)
            except ValueError:
                pass
        if args.best_time:
            score.best_time = str_to_timedelta(args.best_time)
        if args.prize_given:
            score.prize_given = args.prize_given
        sqla_session.commit()

    def get(self):
        """
        Returns the gamer's data
        """
        rp = reqparse.RequestParser()
        rp.add_argument('promo_code', type=unicode, required=True)
        rp.add_argument('game_name', type=unicode)
        args = rp.parse_args()

        try:
            match = re.search(r'[7|8]?(\d{10})', args.promo_code)
            if match:
                phone = match.group(1)
                gamer = Gamer.query.filter_by(phone=phone, is_prize_given=False).one()
            else:
                gamer = Gamer.query.filter_by(promo_code=args.promo_code, is_prize_given=False).one()
        except NoResultFound:
            return 'Gamer not found', 404
        res = {}
        res.update({
            'name': gamer.name,
            'surname': gamer.surname,
            # 'age': gamer.age,
            'phone': gamer.phone,
            'promo_code': gamer.promo_code,
            'prize_given': gamer.is_prize_given
        })
        if args.game_name:
            score = Score.query \
                .filter(
                    Gamer.id == gamer.id,
                    Score.game_name == args.game_name
                ) \
                .join(Score.gamer) \
                .first()
            if score is None:
                res['participate'] = 0
                res['score'] = 0
                res['photos'] = 0
                res['best_time'] = ''
                res['most_pins'] = ''
            else:
                res['participate'] = score.participate
                res['score'] = score.score
                res['photos'] = score.photos
                res['most_pins'] = score.most_pins if score.most_pins > 0 else ''
                if score.best_time and score.best_time > timedelta(0):
                    res['best_time'] = timedelta_to_str(score.best_time)
                else:
                    res['best_time'] = ''
        return res


class GetScoreboard(Resource):
    def get(self):
        sum_score_func = func.sum(Score.score + Score.participate + Score.photos).label('sum_score')
        scores_main = sqla_session.query(Gamer, sum_score_func) \
            .join(Gamer.scores_assoc) \
            .filter(Gamer.is_prize_given.is_(False)) \
            .group_by(Gamer) \
            .having(sum_score_func > 0) \
            .order_by(desc('sum_score'), Gamer.surname, Gamer.name) \
            .limit(50) \
            .all()
        res_main = []
        for r in scores_main:
            d = {'promo_code': r[0].promo_code,
                 'name': r[0].name,
                 'surname': r[0].surname,
                 'score': r[1]}
            res_main.append(d)

        scores_dance = sqla_session.query(Gamer, Score.most_pins) \
            .join(Gamer.scores_assoc) \
            .filter(Gamer.is_prize_given.is_(False),
                    Score.most_pins > 0) \
            .order_by(desc(Score.most_pins), Gamer.surname, Gamer.name) \
            .limit(50) \
            .all()
        res_dance = []
        for r in scores_dance:
            d = {'promo_code': r[0].promo_code,
                 'name': r[0].name,
                 'surname': r[0].surname,
                 'most_pins': r[1]}
            res_dance.append(d)

        scores_autosim = sqla_session.query(Gamer, Score.best_time) \
            .join(Gamer.scores_assoc) \
            .filter(Gamer.is_prize_given.is_(False),
                    Score.best_time > timedelta(0)) \
            .order_by(Score.best_time, Gamer.surname, Gamer.name) \
            .limit(50) \
            .all()
        res_autosim = []
        for r in scores_autosim:
            best_time = timedelta_to_str(r[1]) if r[1] else u""
            d = {'promo_code': r[0].promo_code,
                 'name': r[0].name,
                 'surname': r[0].surname,
                 'best_time': best_time}
            res_autosim.append(d)

        return {'main': res_main, 'dance': res_dance, 'autosim': res_autosim}


class GetGamerSummary(Resource):
    def get(self):
        rp = reqparse.RequestParser()
        rp.add_argument('promo_code', type=unicode, required=True)
        args = rp.parse_args()

        try:
            match = re.search(r'[7|8]?(\d{10})', args.promo_code)
            if match:
                phone = match.group(1)
                gamer = Gamer.query.filter_by(phone=phone, is_prize_given=False).one()
            else:
                gamer = Gamer.query.filter_by(promo_code=args.promo_code, is_prize_given=False).one()
        except NoResultFound:
            return 'Gamer not found', 404
        sum_score = sqla_session.query(Gamer, func.sum(Score.score +
                                                       Score.participate +
                                                       Score.photos).label('sum_score')) \
            .join(Gamer.scores_assoc) \
            .filter(Gamer.is_prize_given.is_(False),
                    Gamer.id == gamer.id) \
            .group_by(Gamer) \
            .first()
        best_time = sqla_session.query(Gamer, func.max(Score.best_time).label('best_time')) \
            .join(Gamer.scores_assoc) \
            .filter(Gamer.is_prize_given.is_(False),
                    Gamer.id == gamer.id) \
            .group_by(Gamer) \
            .first()
        most_pins = sqla_session.query(Gamer, func.max(Score.most_pins).label('most_pins')) \
            .join(Gamer.scores_assoc) \
            .filter(Gamer.is_prize_given.is_(False),
                    Gamer.id == gamer.id) \
            .group_by(Gamer) \
            .first()

        res = {
            'name': gamer.name,
            'surname': gamer.surname,
            'promo_code': gamer.promo_code,
            'score': sum_score[1] if sum_score and sum_score[1] else None,
            'best_time': timedelta_to_str(best_time[1]) if best_time and best_time[1] else None,
            'most_pins': most_pins[1] if most_pins and most_pins[1] else None
        }
        return res


class GetTotal(Resource):
    def get(self):
        total = sqla_session.query(func.count(Gamer.id)).one()
        return {'total': total[0]}


endpoint.add_resource(SearchByPromoCode, '/search_by_phone')
endpoint.add_resource(MangleGamer, '/mangle_gamer')
endpoint.add_resource(GetScoreboard, '/get_scoreboard')
endpoint.add_resource(GetGamerSummary, '/get_gamer_summary')
endpoint.add_resource(GetTotal, '/total')