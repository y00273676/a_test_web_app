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
tmp_path = "/home/test/tmp/push"

class PushHandler(BaseHandler):
    def get(self, op):
        name = '推荐'
        if op == None:
            user = self.get_current_user()
            items = ctrl.api.get_all('push')
            self.render('tmp.tpl', user=user, items=items, name=name)
            return

        if op == 'add':
            user = self.get_current_user()
            self.render('new_tmp.tpl', user=user, name=name)

        if op == 'del':
            id = int(self.get_argument('id', 0))
            ctrl.api.delete_by_id('push', id)
            self.redirect('/push')

        if op == 'edit':
            pass
        if op == 'pub':
            num = int(self.get_argument('id', 0))
            output = str(self.get_argument('output', ''))
            product = str(self.get_argument('product', ''))
            version = str(self.get_argument('version', ''))
            product = PRODUCT_PATH[PRODUCT.index(product)]
            path = PUB_PATH.format('push', output, product)
            version_path = VERSION_PATH.format('push', output, product)
            songList = {
                "id": "",
                "name": "",
                "singer": "",
                "language": ""
            }
            info = {
                "name": "",
                "picture": "",
                "des": "",
                "subPicture": "",
                "title":"",
                "songList":[]
            }
            pub_json = {
                "version": "",
                "info":[]
            }

            pub_json['version'] = version

            file_txt = commands.getoutput('ls {}tuijian*.txt'.format(path))
            file_pic = commands.getoutput('ls {}*.png'.format(path))
            file_txt = file_txt.split('\n')
            file_des = os.path.join(path, 'song_desc.txt')
            with open(file_des) as fp:
                for line in fp:
                    line = line.strip('\n')
                    line = line.split('=')
                    info_tmp = copy.deepcopy(info)
                    info_tmp['name'] = line[0]
                    info_tmp['picture'] = line[0]+'.png'
                    info_tmp['des'] = line[1].split('%7C')[1]
                    subPicture = path+line[0]+'1.png'
                    if subPicture in file_pic:
                        info_tmp['subPicture'] = subPicture.replace(path, '')
                    info_tmp['title'] = line[1].split('%7C')[0]
                    pub_json['info'].append(info_tmp)
                    file_tmp = os.path.join(path, info_tmp['name']+'.txt')
                    with open(file_tmp) as fp_song:
                        for line_song in fp_song:
                            line_song = line_song.split('||')
                            song = copy.deepcopy(songList)
                            song['id'] = line_song[0].strip('\n')
                            song['name'] = line_song[1].strip('\n')
                            song['singer'] = line_song[2].strip('\n')
                            song['language'] = line_song[3].strip('\n')
                            info_tmp['songList'].append(song)

            os.system('rm -rf {}'.format(file_des))
            pub_txt = os.path.join(path, 'song_list.json')
            with open(pub_txt, 'w+') as fp:
                fp.write(json.dumps(pub_json))
            pub_src = os.path.join(version_path, 'Newandriod')
            os.system('rm -rf {}*.txt'.format(path))
            os.system('rm -rf {}res/*.png'.format(path))
            os.system('mv {}*.png {}res/'.format(path, path))
            shutil.make_archive(pub_src, 'zip', root_dir=path)
            auth = CDN.auth
            key = ZIP_KEY.format('push', output, product)
            token = auth.upload_token(BUCKET, key, 3600)
            put_file(token, key, pub_src+'.zip')
            ctrl.api.update_pub('push', num, {'is_pub': 1})

            self.redirect('/push')

    def post(self, op):
        if op == 'upload':
            file_meta = self.request.files['file']
            file_name = file_meta[0]['filename']
            file_path = os.path.join(tmp_path, file_name)
            with open(file_path, 'w+') as fp:
                fp.write(file_meta[0]['body'])
            ret = {'name': file_name.split('.')[0]}
            self.send_json(ret)
            return

        if op == 'add_tmp':
            data = {}
            data['name'] = self.get_argument('title', '')
            data['product'] = self.get_argument('product', '')
            data['output'] = self.get_argument('output', '')
            data['describe'] = self.get_argument('desc', '无')
            if '' in data.values() or None in data.values():
                return

            path = int(data['product'])
            data['product'] = PRODUCT[int(data['product'])]
            data['output'] = OUTPUT[int(data['output'])]
            data['version'] = int(str(datetime.now().date()).replace('-',''))
            song_desc = self.request.body.split('&')[7:]
            file_name = os.path.join(tmp_path, 'song_desc.txt')
            with open(file_name, 'w+') as fp:
                for i in song_desc:
                    fp.write(i)
                    fp.write('\n')

            for i in UPLOAD_DEL:
                os.system(i.format('push', data['output'], PRODUCT_PATH[path]))

            for i in UPLOAD_PROC:
                os.system(i.format('push', 'push', data['output'], PRODUCT_PATH[path]))

            os.system(ZIP_PROC.format('push', data['output'], PRODUCT_PATH[path], 'push', data['output'], PRODUCT_PATH[path]))
            os.system(ZIP_DEL.format('push', data['output'], PRODUCT_PATH[path]))

            is_success = ctrl.api.add_product('push', **data)
            if is_success == True:
                self.redirect('/push')
                return
