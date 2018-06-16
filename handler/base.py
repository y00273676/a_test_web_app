#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback
import re

from tornado import web
from lib import uimethods, utils
from const  import COOKIES, USERS, ERR_MSG
from tornado.options import options


class BaseHandler(web.RequestHandler):

    def check_xsrf_cookie(self):
        super(BaseHandler, self).check_xsrf_cookie()

    def _login(self, username):
        self.set_secure_cookie(COOKIES, username, expires_days=1)

    def _logout(self):
        self.clear_cookie(COOKIES)

    @property
    def username(self):
        username = self.get_secure_cookie(COOKIES)
        if username:
            if username.decode() not in USERS:
                self._logout()
                return
        return username

    def get_current_user(self):
        username = self.username
        if not username:
            self._logout()
            return
        return username.decode()

    def dict_args(self):
        _rq_args = self.request.arguments
        rq_args = dict([(k, _rq_args[k][0].decode()) for k in _rq_args])
        logging.info(rq_args)
        return rq_args

    def send_json(self, data={}, errcode=0, errmsg='', status_code=200):
        res = {
            'errcode': errcode,
            'errmsg': ERR_MSG[errcode] if not errmsg else errmsg
        }
        res.update(data)
        json_str = uimethods.json_format(self, res)

        if options.debug:
            logging.info('path: %s, arguments: %s, response: %s'%(self.request.path, self.request.arguments, json_str))

        jsonp = self.get_argument('callback', '')
        if jsonp:
            jsonp = re.sub(r'[^\w\.]', '', jsonp)
            self.set_header('Content-Type', 'text/javascript; charet=UTF-8')
            json_str = '%s(%s)' % (jsonp, json_str)
        else:
            self.set_header('Content-Type', 'application/json')
        self.set_status(status_code)
        self.write(json_str)

    def write_error(self, status_code=200, **kwargs):
        if 'exc_info' in kwargs:
            err_object = kwargs['exc_info'][1]
            traceback.format_exception(*kwargs['exc_info'])

            if isinstance(err_object, utils.ParamError):
                err_info = err_object.kwargs
                logging.error(err_info)
                self.send_json(**err_info)
                return

        if not options.debug:
            self.captureException(**kwargs)

    def jrender(self, tpl, **kwargs):
        if self.get_argument('js', ''):
            self.set_header('Access-Control-Allow-Origin', '*')
            self.send_json(kwargs)
        else:
            self.render(tpl, **kwargs)

    def has_argument(self, name):
        return name in self.request.arguments

    def log_sentry(self, data):
        self.captureMessage(data, stack=True)

