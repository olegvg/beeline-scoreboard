# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import traceback
from flask.ext.restful import Api as BaseApi
from flask import current_app, make_response
from json import dumps


class Api(BaseApi):
    def __init__(self, *args, **kwargs):
        super(Api, self).__init__(*args, **kwargs)
        self.representations = {
            'application/json': self.unicode_output_json
        }

    @staticmethod
    def unicode_output_json(data, code, headers=None):
        """Makes a Flask response with a JSON encoded unicode-aware body """

        settings = {
            'ensure_ascii': False,
            'encoding': 'utf8'
        }
        if current_app.debug:
            settings.update({
                'indent': 4,
                'sort_keys': True
            })

        dumped = dumps(data, **settings)
        if 'indent' in settings:
            dumped += '\n'

        resp = make_response(dumped, code)
        resp.headers.extend(headers or {})
        return resp

    def handle_error(self, e):
        code = getattr(e, 'code', 500)
        if code == 500:      # for HTTP 500 errors return my custom response
            current_app.logger.error(traceback.format_exc())
            return self.make_response({'message': "something went wrong, i'll fix it soon", 'error_code': 'no idea'}, 500)
        return super(Api, self).handle_error(e)


