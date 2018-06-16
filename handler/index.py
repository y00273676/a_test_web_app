#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import math
import uuid
import base64
import hmac
import time
import logging
import when
import random
from datetime import datetime, timedelta
from urllib import quote, unquote, urlencode
from hashlib import sha1, md5
from tornado import web, gen
from handler.base import BaseHandler
from tornado import httpclient, web
from tornado.gen import coroutine
from const import USERS
import pdb

class IndexHandler(BaseHandler):
    def get(self):
        uname = self.get_current_user()
        if not uname:
            self.redirect('/login')
            return
        self.render('index.tpl', user=uname)

    def post(self):
        pass


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.tpl', errmsg='')
        return
    def post(self):
        _res = {}
        _res['code'] = 1
        _res['msg'] = "登录失败！"

        uname = self.get_argument('uname', '')
        passwd = self.get_argument('passwd', '')

        if int(passwd) == USERS.get(uname, 0):
            self._login(uname)
            _res['code'] = 0
            _res['msg'] = '登陆成功'
            self.set_secure_cookie('uname', uname)
            self.send_json(_res)
            self.redirect('/')
        else:
            self.send_json(_res)
        return



class LogoutHandler(BaseHandler):
    def get(self):
        self.redirect('/login')
        return
    def post(self):
        pass

