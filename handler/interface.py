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
from control import ctrl
from const import PRODUCT,OUTPUT, MSGID, PUSH_MSG_ID
tmp_path = '/home/test/tmp/auth'
class JyauthHandler(BaseHandler):
    @gen.coroutine
    def get(self, op):
        if op == None:
            user = self.get_current_user()
            self.render('auth.tpl', user=user)
            return
        if op == 'upload':
            add_mac = self.get_argument('add_mac', '')
            del_mac = self.get_argument('del_mac', '')
            if add_mac != None and add_mac != '':
                ctrl.api.add_one_auth(add_mac.upper())

            if del_mac != None and del_mac != '':
                ctrl.api.del_one_auth(del_mac.upper())
            ret = {}
            ret['code'] = 1
            self.send_json(ret)
        if op == 'addmeal':
            ret = {}
            mac = self.get_argument('mac', '')
            meal = self.get_argument('meal', '')
            if mac == '':
                ret['code'] = 0
                self.send_json(ret)
                return
            mac = mac.replace(':', '').lower()
            uid = ctrl.api.get_uid(mac)
            if not uid:
                ret['code'] = 0
                self.send_json(ret)
                return
            msgid = MSGID[int(meal)]
            respose = yield httpclient.AsyncHTTPClient().fetch(PUSH_MSG_ID.format(uid, msgid)) 
            ret['code'] = json.loads(respose.body)['status']
            self.send_json(ret)

    def post(self):
        file_meta = self.request.files['file']
        file_name = file_meta[0]['filename']
        file_path = os.path.join(tmp_path, file_name)
        with open(file_path, 'w+') as fp:
            fp.write(file_meta[0]['body'])

        data = {}
        with open(file_path, 'r') as fp:
            for line in fp:
                data['mac'] = line.upper()
                ctrl.api.add_auth(**data)

        ret = {'name': file_name.split('.')[0]}
        self.send_json(ret)
        return
