#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from tornado.options import options
from tornado.log import access_log
import openpyxl
from openpyxl.styles import Alignment
from tornado import web, gen, httpclient
import logging
import json
from tornado.gen import coroutine
from tornado.httputil import url_concat
import datetime
import requests
import time
import pprint
from qiniu import Auth, put_file, BucketManager
import redis
import pylibmc
from const import *
from lib.decorator import DictProperty

class Qiniu(object):
    # qiniu python sdk
    def __init__(self, ak, sk):
        self.ak, self.sk, self.config = ak, sk, {}

    @DictProperty('config', 'Qiniu.auth', True)
    def auth(self):
        return Auth(self.ak, self.sk)


def log_func(handler):
    if handler.get_status() < 400:
        log_method = access_log.info
    elif handler.get_status() < 500:
        log_method = access_log.warning
    else:
        log_method = access_log.error
    request_time = 1000.0 * handler.request.request_time()
    log_method("%d  %s  %s  %.2fms \n (%s) \n %s",
        handler.get_status(),
        handler.request.method,
        handler.request.remote_ip,
        request_time,
        handler.request.uri,
        pprint.pformat(handler.request.arguments))

def get_cur_info():
    print sys._getframe().f_code.co_filename
    print sys._getframe(0).f_code.co_name
    print sys._getframe(1).f_code.co_name
    print sys._getframe().f_lineno

class Memcached(object):

    def __init__(self, servers, binary=True, behaviors={'tcp_nodelay': True, 'ketama': True}):
        self.client = pylibmc.Client(servers, binary=binary, behaviors=behaviors)

    def __getattr__(self, attr):
        return self.client.get(attr)

CDN = Qiniu(AK, SK)
mc = Memcached(MEMCACHE)
redisc = redis.StrictRedis(host=REDIS['salve']['host'], port=REDIS['salve']['port'], db=REDIS['salve']['db'])
