#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import uuid
import base64

from tornado import web
from tornado.options import options
from lib import uimodules, uimethods
from tornado.httpserver import HTTPServer
#from raven.contrib.tornado import AsyncSentryClient
from lib.utils import log_func

URLS = [
    (r'new_web_manage\.90iktv\.com',
        (r'/?', 'handler.index.IndexHandler'),
        (r'/login', 'handler.index.LoginHandler'),
        (r'/logout', 'handler.index.LogoutHandler'),
        (r'/jyauth/?(add|upload|get|del|addmeal)?', 'handler.interface.JyauthHandler'),
        (r'/push/?(add_tmp|upload|count|pub|add|del|edit)?', 'handler.push.PushHandler'),
        (r'/rank/?(add_tmp|upload|count|pub|add|del|edit)?', 'handler.rank.RankHandler'),
        (r'/class/?(add_tmp|upload|count|pub|add|del|edit)?', 'handler.class.ClassHandler'),
        (r'/db/?(test|verify|test_pub|verify_pub|get_db)?', 'handler.db.DbHandler'),
     )
]

class Application(web.Application):

    def __init__(self):
        settings = {
            'login_url': '/login',
            # 'xsrf_cookies': True,
            'compress_response': True,
            'debug': options.debug,
            'log_function': log_func,
            'ui_modules': uimodules,
            'ui_methods': uimethods,
            'static_path': os.path.join(sys.path[0], 'www/layui'),
            'template_path': os.path.join(sys.path[0], 'www'),
            'cookie_secret': base64.b64encode(uuid.uuid3(uuid.NAMESPACE_DNS, 'new_web_manage').bytes),
            #'sentry_url': 'https://5d87deb2186046dda0db4bf050539dd2:214281f0893c4f8984f247ee38c27f46@sentry.ktvsky.com/7'# if not options.debug else ''
        }
        web.Application.__init__(self, **settings)

        for spec in URLS:
            host = '.*$'
            handlers = spec[1:]
            self.add_handlers(host, handlers)


def run():
    app = Application()
    #app.sentry_client = AsyncSentryClient(app.settings['sentry_url'])
    http_server = HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    print('Running on port %d' % options.port)

