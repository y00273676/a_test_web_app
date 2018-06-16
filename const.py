#!/usr/bin/env python
# -*- coding: utf-8 -*-

# web_manage user manage
USERS = {'123456': 123456}
COOKIES = 'new_web_manage'
ERR_MSG = {
    0: '服务正常',
    -1: '参数错误',
    -2: '请求的资源不存在',
    404: '无数据',
    20001: '手机号码格式有误,请检查!',
    20002: '手机号已经被注册过，请查询后重新发送！',
    20003: '注册成功',
    30001: '频繁结算，请稍后再试',
    30002: '无效日期，无法生成理财策略模型方案',

    40000: '数据操作失败',
    40001: '无权限'
}

AK = 'wkPHVweSOSuIg8FluQxH8ow0aSzq_VkLYPpKJznm'
SK = 'SrQ-PKa2hQYOJmC4K0aMBNqj1xZsaNDslLlPpP22'

REDIS = {
    'master':{
        'host': '10.9.45.52',
        'port': 6379,
        'db': 0
    },
    'salve':{
        'host': '10.9.37.73',
        'port': 6379,
        'db': 0
    }
}

MEMCACHE = ['10.9.53.253:11211']

DB_ANDRIOD = 'andriod'
DB_PRODUCT = 'product_manage'
DB_USER = 'leike_user'
MYSQL_KTV = {
    DB_ANDRIOD: {
        'master': {
            'host': '10.9.36.50',
            'user': 'root',
            'pass': 'SkyrockerUdb0',
            'port': 3306
        },
        'slaves': [
            {
                'host': '10.9.61.98',
                'user': 'root',
                'pass': 'SkyrockerUdb0',
                'port': 3306
            }
        ]
    },
    DB_PRODUCT: {
        'master': {
            'host': '10.9.36.50',
            'user': 'root',
            'pass': 'SkyrockerUdb0',
            'port': 3306
        },
        'slaves': [
            {
                'host': '10.9.61.98',
                'user': 'root',
                'pass': 'SkyrockerUdb0',
                'port': 3306
            }
        ]
    },
    DB_USER: {
        'master': {
            'host': '10.9.36.50',
            'user': 'root',
            'pass': 'SkyrockerUdb0',
            'port': 3306
        },
        'slaves': [
            {
                'host': '10.9.61.98',
                'user': 'root',
                'pass': 'SkyrockerUdb0',
                'port': 3306
            }
        ]
    }
}
BUCKET = 'ktvdaren'
BUCKET_PRI = '77gais.com2.z0.glb.qiniucdn.com'

PRODUCT = ['云十二PRO','惊艳PLUS','云十二PLUS']
PRODUCT_PATH = ['y_pro','j_plus','y_plus']
OUTPUT = ['TV','VGA','IOS','ANDRIOD']
PUB_PATH = "/home/test/tmp/{}/{}/{}/"
VERSION_PATH = "/home/test/tmp/{}/{}/version/{}/"
UPLOAD_PROC = [
    'mv /home/test/tmp/{}/*.txt /home/test/tmp/{}/{}/{}/',
    'mv /home/test/tmp/{}/*.js /home/test/tmp/{}/{}/{}/',
    'mv /home/test/tmp/{}/*.zip /home/test/tmp/{}/{}/{}/'
]
UPLOAD_DEL = [
    'rm -rf /home/test/tmp/{}/{}/{}/*.txt',
    'rm -rf /home/test/tmp/{}/{}/{}/*.js',
    'rm -rf /home/test/tmp/{}/{}/{}/*.png',
    'rm -rf /home/test/tmp/{}/{}/{}/*.zip',
    'rm -rf /home/test/tmp/{}/{}/{}/*.json',
    'rm -rf /home/test/tmp/{}/{}/{}/res/*.png'
]
ZIP_PROC = 'unzip  /home/test/tmp/{}/{}/{}/*.zip -d /home/test/tmp/{}/{}/{}/'
ZIP_DEL = 'rm -rf /home/test/tmp/{}/{}/version/{}/*.zip'
ZIP_KEY = "/Newandriod/{}/{}/{}/Newandriod.zip"

SQL_DEL = [
    'delete from KTV_MEDIAS_INFO;',
    'delete from KTV_ACTOR_INFO;',
]

SQL_FTS_DEL = 'delete from medias;'

MYSQL_DEL = [
    'rm -rf /data/db/media.sql',
    'rm -rf /data/db/actor.sql',
    'rm -rf /data/db/medias.sql'
]

MYSQL_TMP = [
    'drop table media_tmp;',
    'drop table actor_tmp;',
    'create table media_tmp (select * from medias order by media_click desc);',
    'create table actor_tmp (select * from actors order by actor_click desc);'
]

MYSQL_DUMP = [
    'mysqldump -t  --skip-extended-insert -h10.9.36.50 -uroot -pSkyrockerUdb0  --databases andriod --tables media_tmp>/data/db/media.sql',
    'mysqldump -t  --skip-extended-insert -h10.9.36.50 -uroot -pSkyrockerUdb0  --databases andriod --tables actor_tmp>/data/db/actor.sql',
]

MYSQL_SED = [
    'cp /data/db/media.sql /data/db/medias.sql',
    'sed -i "s/media_tmp/KTV_MEDIAS_INFO/g" /data/db/media.sql',
    'sed -i "s/actor_tmp/KTV_ACTOR_INFO/g" /data/db/actor.sql',
    'sed -i "s/media_tmp/medias/g" /data/db/medias.sql'

]

MYSQL_SQLITE = [
    'mysql2sqlite /data/db/media.sql | sqlite3 /data/db/andriod.db',
    'mysql2sqlite /data/db/medias.sql | sqlite3 /data/db/fts_medias.db',
    'mysql2sqlite /data/db/actor.sql | sqlite3 /data/db/andriod.db'
]

VERSION_KEY = '/Newandriod_test/update_db/version.txt'

VERSION_KEY_NEW = '/Newandriod/update_db/version.txt'

DB_KEY = '/Newandriod_test/update_db/andriod.zip'

DB_KEY_NEW = '/Newandriod/update_db/andriod.zip'

JY_JB = 'SR3719c_JY_{}'

MEAL_DETAILS = ['三年下载','两年下载','一年下载']
MEALID = [23, 24, 21]

PUSH_MSG_ID = 'http://box.90iktv.com/dealpushedmsg?userid={}&msgid={}&newadd=1'
MSGID = [21, 22, 17]
