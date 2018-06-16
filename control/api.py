#!/usr/bin/env python
# -*- coding: utf-8 -*-

from const import MEAL_DETAILS, MEALID

class APICtrl(object):

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.api = ctrl.pdb.api

    def __getattr__(self, name):
        return getattr(self.api, name)

    def update_user_meal(self, uid, meal):
        details = MEAL_DETAILS[int(meal)]
        mealid = MEALID[int(meal)]
        self.api.update_user_api(uid, mealid, abs(int(meal)-3), details)
        return


