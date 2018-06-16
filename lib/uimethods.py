#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

def json_format(handler, res):

    def _format(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, Decimal):
            return ('%.2f' % obj)
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')

    return json.dumps(res, default=_format)

