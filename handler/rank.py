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
tmp_path = "/home/test/tmp/rank"

class RankHandler(BaseHandler):
    def get(self, op):
        name = '榜单'
        if op == None:
            user = self.get_current_user()
            items = ctrl.api.get_all('rank')
            self.render('tmp.tpl', user=user, items=items, name=name)
            return

        if op == 'add':
            user = self.get_current_user()
            self.render('new_tmp.tpl', user=user, name=name)

        if op == 'del':
            id = int(self.get_argument('id', 0))
            ctrl.api.delete_by_id('rank', id)
            self.redirect('/rank')

        if op == 'edit':
            pass
        if op == 'pub':
            num = int(self.get_argument('id', 0))
            output = str(self.get_argument('output', ''))
            product = str(self.get_argument('product', ''))
            version = str(self.get_argument('version', ''))
            product = PRODUCT_PATH[PRODUCT.index(product)]
            path = PUB_PATH.format('rank', output, product)
            version_path = VERSION_PATH.format('rank', output, product)
            addr_json = {"data":[]}
            addr_pic = {
                "name": "",
                "state": "",
                "type": "",
                "x": "",
                "y": "",
                "width": "",
                "height": "",
                "picture": ""
            }
            addr_font = {
                "name": "",
                "state": "",
                "type": "",
                "title": "",
                "x": "",
                "y": "",
                "width": "",
                "height": "",
                "style": {
                    "font-family": "",
                    "font-size": "",
                    "color": "",
                    "letter-spacing": "",
                    "text-align": ""
                }
            }
            file_data = commands.getoutput("ls {}*.js".format(path))
            png_data = commands.getoutput("ls {}*.png".format(path))
            png_data = png_data.split("\n")
            for i,j in enumerate(png_data):
                png_data[i] = j.replace(path, "")

            with open(file_data) as fp:
                line = fp.readline()
                line = line.replace('var pageData = ', '')
                line = eval(line)
                line = line["artboard"].items()[0][1]["layer"]
                line.pop(0)
                for i in line:
                    if i["name"].endswith("_normal"):
                        pictures = copy.deepcopy(addr_pic)
                        png_tmp = i['src']+'@1x.png'
                        if png_tmp in png_data:
                            os.system("mv {}{} {}{}".format(path, png_tmp, path, i['name']+'.png'))
                            os.system("mv {}{} {}{}".format(path, i['name']+'.png', path, 'res/'))

                        for j in pictures.keys():
                            if j in i.keys():
                                pictures[j] = i[j]
                        pictures["picture"] = i["name"].replace("_normal", ".png")
                        pictures["state"] = "normal"
                        pictures["name"] = i["name"].replace("_normal", "")
                        addr_json["data"].append(pictures)
                    if i["name"].endswith("_main"):
                        font = copy.deepcopy(addr_font)
                        for j in font.keys():
                            if j in i.keys():
                                font[j] = i[j]
                        font["title"] = i["html"]
                        font["state"] = "main"
                        font["name"] = i["name"].replace("_main", "")
                        addr_json["data"].append(font)

            song_text = commands.getoutput("ls {}*.txt".format(path))
            song_text = song_text.split('\n')
            song_json = {
                "version": "",
                "info": []
            }
            info_list = {
                "name": "",
                "songList": []
            }
            song_list = {
                "id": "",
                "name": "",
                "singer": "",
                "language": ""
            }
            for song_tmp in song_text:
                info_tmp = copy.deepcopy(info_list)
                info_tmp["name"] = song_tmp.replace(path, "").replace(".txt", "")
                with open(song_tmp) as fp:
                    for line in fp:
                        line_song = line.split("||")
                        song = copy.deepcopy(song_list)
                        song['id'] = line_song[0].strip('\n')
                        song['name'] = line_song[1].strip('\n')
                        song['singer'] = line_song[2].strip('\n')
                        song['language'] = line_song[3].strip('\n')
                        info_tmp["songList"].append(song)
                song_json["info"].append(info_tmp)

            song_json["version"] = version
            os.system("rm -rf {}*.txt".format(path))
            os.system("rm -rf {}*.js".format(path))
            address = os.path.join(path, "ui.json")
            song_info = os.path.join(path, "song_list.json")

            with open(address, 'w+') as fp:
                fp.write(json.dumps(addr_json))

            with open(song_info, 'w+') as fp:
                fp.write(json.dumps(song_json))

            pub_src = os.path.join(version_path, 'Newandriod')
            os.system('rm -rf {}*.png'.format(path))
            os.system('rm -rf {}*.zip'.format(path))
            shutil.make_archive(pub_src, 'zip', root_dir=path)
            auth = CDN.auth
            key = ZIP_KEY.format('rank', output, product)
            token = auth.upload_token(BUCKET, key, 3600)
            put_file(token, key, pub_src+'.zip')
            ctrl.api.update_pub('rank', num, {'is_pub': 1})

            self.redirect('/rank')

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

            for i in UPLOAD_DEL:
                os.system(i.format('rank', data['output'], PRODUCT_PATH[path]))

            for i in UPLOAD_PROC:
                os.system(i.format('rank', 'rank', data['output'], PRODUCT_PATH[path]))

            os.system(ZIP_PROC.format('rank', data['output'], PRODUCT_PATH[path], 'rank', data['output'], PRODUCT_PATH[path]))
            os.system(ZIP_DEL.format('rank', data['output'], PRODUCT_PATH[path]))

            is_success = ctrl.api.add_product('rank', **data)
            if is_success == True:
                self.redirect('/rank')
                return

