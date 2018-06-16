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
import commands
import copy
import shutil
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from datetime import datetime, timedelta
from urllib import quote, unquote, urlencode
from hashlib import sha1, md5
from tornado import web, gen
from handler.base import BaseHandler
from tornado import httpclient, web
from tornado.gen import coroutine
from control import ctrl
from const import *
from lib.utils import CDN
from qiniu import put_file
import MySQLdb
import sqlite3

class DbHandler(BaseHandler):
    def get(self, op):
        if op == 'test':
            name = "测试"
            user = self.get_current_user()
            items = ctrl.api.get_db_all('test')
            self.render('db.tpl', user=user, items=items, name=name)
            return

        if op == 'verify':
            name = "发布"
            user = self.get_current_user()
            items = ctrl.api.get_db_all('verify')
            self.render('db.tpl', user=user, items=items, name=name)

        if op == 'test_pub':
            q = CDN.auth
            sql_conn = sqlite3.connect('/data/db/andriod.db', check_same_thread=False)
            s_cursor = sql_conn.cursor()

            sql_conn_fts = sqlite3.connect('/data/db/fts_medias.db', check_same_thread=False)
            s_cursor_fts = sql_conn_fts.cursor()
            #清空sqlite中的表
            for i in SQL_DEL:
                s_cursor.execute(i)
            sql_conn.commit()
            s_cursor_fts.execute(SQL_FTS_DEL)
            sql_conn_fts.commit()
            conn = MySQLdb.connect(host='10.9.36.50', port=3306, passwd='SkyrockerUdb0', user='root', db='andriod', charset='UTF8')
            cursor = conn.cursor()

            for i in MYSQL_DEL:
                os.system(i)

            for i in MYSQL_TMP:
                cursor.execute(i)
            conn.commit()
            conn.close()
            for i in MYSQL_DUMP:
                os.system(i)

            for i in MYSQL_SED:
                os.system(i)

            for i in MYSQL_SQLITE:
                os.system(i)

            for i in MYSQL_DEL:
                os.system(i)

            shutil.make_archive('/data/db_version/andriod', 'zip', root_dir='/data/db')

            token = q.upload_token(BUCKET, DB_KEY, 3600)
            localfile = '/data/db_version/andriod.zip'
            ret, info = put_file(token, DB_KEY, localfile)

            data = {'db':'test', 'version': int(str(datetime.now().date()).replace('-',''))}
            ctrl.api.add_db(**data)

            sql_conn.commit()
            sql_conn.close()
            sql_conn_fts.commit()
            sql_conn_fts.close()
            self.redirect('/db/test')

        if op == 'verify_pub':
            q = CDN.auth
            token = q.upload_token(BUCKET, DB_KEY_NEW, 3600)
            localfile = '/data/db_version/andriod.zip'
            ret, info = put_file(token, DB_KEY, localfile)
            data = {'db':'verify', 'version': int(str(datetime.now().date()).replace('-',''))}
            ctrl.api.add_db(**data)

            self.redirect('/db/verify')

        if op == 'get_db':
            q = CDN.auth
            base_url = 'http://{}/{}'.format(BUCKET_PRI, DB_KEY)
            private_url = q.private_download_url(base_url, expires=3600)

            self.redirect(private_url)
