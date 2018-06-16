#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TINYINT, TEXT, DATETIME
from orm.base import NotNullColumn, Base, ModelBase
from lib.decorator import model_to_dict, models_to_list, close_conn
from const import DB_ANDRIOD, DB_PRODUCT, DB_USER, JY_JB
from sqlalchemy.sql.expression import func
import datetime
from sqlalchemy import Column
from sqlalchemy.sql.expression import func, desc, asc, or_

class Class(Base):
    '''
    分类数据管理
    '''
    __tablename__ = 't_class'

    id = Column(INTEGER(11), primary_key=True)
    name = NotNullColumn(VARCHAR(128), default='0')
    product  = NotNullColumn(VARCHAR(128), default='')
    output = NotNullColumn(VARCHAR(128), default='')
    describe = Column(TEXT)
    version = NotNullColumn(INTEGER(11), default=0)
    is_pub = NotNullColumn(TINYINT, default=0)

class Push(Base):
    '''
    推荐数据管理
    '''
    __tablename__ = 't_push'
    id = Column(INTEGER(11), primary_key=True)
    name = NotNullColumn(VARCHAR(128), default='0')
    product  = NotNullColumn(VARCHAR(128), default='')
    output = NotNullColumn(VARCHAR(128), default='')
    describe = Column(TEXT)
    version = NotNullColumn(INTEGER(11), default=0)
    is_pub = NotNullColumn(TINYINT, default=0)

class Rank(Base):
    '''
    榜单数据管理
    '''
    __tablename__ = 't_rank'
    id = Column(INTEGER(11), primary_key=True)
    name = NotNullColumn(VARCHAR(128), default='0')
    product  = NotNullColumn(VARCHAR(128), default='')
    output = NotNullColumn(VARCHAR(128), default='')
    describe = Column(TEXT)
    version = NotNullColumn(INTEGER(11), default=0)
    is_pub = NotNullColumn(TINYINT, default=0)

class DB(Base):
    '''
    榜单数据管理
    '''
    __tablename__ = 't_db'
    id = Column(INTEGER(11), primary_key=True)
    db = Column(VARCHAR(64))
    version = NotNullColumn(INTEGER(11), default=0)

class Auth(Base):
    '''
    榜单数据管理
    '''
    __tablename__ = 'jy_jb'
    id = Column(INTEGER(11), primary_key=True)
    mac = NotNullColumn(VARCHAR(256), default='0')


class UserInfo(ModelBase):
    """用户设备信息"""

    __tablename__ = 'userinfo'

    uid = Column(INTEGER(11), primary_key=True)
    uname = Column(VARCHAR(32))
    upwd = Column(VARCHAR(32))
    utime = Column(DATETIME)
    ustate = Column(INTEGER(11))
    uphone = Column(VARCHAR(32))
    uaddress = Column(VARCHAR(256))
    uemail = Column(VARCHAR(128))
    unick = Column(VARCHAR(64))
    uremark = Column(VARCHAR(512))


class UserMeal(ModelBase):
    """用户设备信息"""

    __tablename__ = 'user_meal'

    id = Column(INTEGER(11), primary_key=True)
    uid = Column(INTEGER(11))
    starttime = Column(DATETIME)
    endtime = Column(DATETIME)
    utype = Column(INTEGER(11))
    addtime = Column(DATETIME)
    details = Column(VARCHAR(1024))
    state = Column(INTEGER(11))
    totals = Column(INTEGER(11))
    lasttotal = Column(INTEGER(11))
    mealid = Column(INTEGER(11))
    tradeno = Column(VARCHAR(64))


class APIModel(object):
    def __init__(self , pdb):
        self.pdb = pdb
        self.master = pdb.get_session(DB_ANDRIOD, master=True)
        self.slave = pdb.get_session(DB_ANDRIOD)
        self.auth_master = pdb.get_session(DB_PRODUCT, master=True)
        self.auth_slave = pdb.get_session(DB_PRODUCT)
        self.user_master = pdb.get_session(DB_USER, master=True)
        self.user_slave = pdb.get_session(DB_USER)

    @close_conn(name='slave')
    @models_to_list
    def get_all(self, product):
        if product == 'push':
            tmp = self.slave.query(Push).order_by(Push.update_time.desc()).offset(0).limit(12)
        if product == 'class':
            tmp = self.slave.query(Class).order_by(Class.update_time.desc()).offset(0).limit(12)
        if product == 'rank':
            tmp = self.slave.query(Rank).order_by(Rank.update_time.desc()).offset(0).limit(12)
        return tmp.all()

    @close_conn(name='slave')
    @models_to_list
    def get_db_all(self, db):
        tmp = self.slave.query(DB).filter(DB.db==db).order_by(DB.update_time.desc()).offset(0).limit(12)
        return tmp.all()

    @close_conn(name='master')
    def add_db(self, **data):
        tmp  = DB(**data)
        self.master.add(tmp)
        self.master.commit()
        return True

    @close_conn(name='master')
    def add_product(self, prduct, **data):
        if prduct == 'rank':
            tmp  = Rank(**data)
        if prduct == 'push':
            tmp  = Push(**data)
        if prduct == 'class':
            tmp  = Class(**data)
        self.master.add(tmp)
        self.master.commit()
        return True

    @close_conn(name='auth_master')
    def add_auth(self, **data):
        tmp = Auth(**data)
        self.auth_master.add(tmp)
        self.auth_master.commit()
        return True

    @close_conn(name='auth_master')
    def add_one_auth(self, mac):
        tmp = Auth()
        tmp.mac = mac
        self.auth_master.add(tmp)
        self.auth_master.commit()
        return True

    @close_conn(name='auth_master')
    def del_one_auth(self, mac):
        self.auth_master.query(Auth).filter(Auth.mac==mac).delete()
        self.auth_master.commit()
        return True

    @close_conn(name='master')
    def delete_by_id(self, product, id):
        if product == 'rank':
            self.master.query(Rank).filter(Rank.id==id).delete()
        if product == 'push':
            self.master.query(Push).filter(Push.id==id).delete()
        if product == 'class':
            self.master.query(Class).filter(Class.id==id).delete()
        self.master.commit()
        return True

    @close_conn(name='master')
    def update_pub(self, product, num, data):
        if product == 'push':
            self.master.query(Push).filter_by(id=num).update(data)
        if product == 'class':
            self.master.query(Class).filter_by(id=num).update(data)
        if product == 'rank':
            self.master.query(Rank).filter_by(id=num).update(data)
        self.master.commit()
        return True

    @close_conn(name='user_slave')
    def get_uid(self, mac):
        name = JY_JB.format(mac)
        q = self.user_slave.query(UserInfo.uid).filter(UserInfo.uname==name).all()
        return q[0][0] if q else None

    @close_conn(name='user_master')
    def update_user_api(self, uid, meal, years, details):
        user = UserMeal()
        user.uid, user.mealid, user.state, user.utype, user.details = uid, meal, 1, 1, details
        user.starttime = datetime.datetime.now()
        user.endtime = user.starttime.replace(year = user.starttime.year+years)
        self.user_master.add(user)
        self.user_master.commit()
        return True
