#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: internal_message.py
# @time: 2019/5/13 10:46
# @Software: PyCharm


__author__ = 'A.Star'

from snowland_py253.account import Account
import requests
import datetime
from snowland_py253.common import (
    PY253_SMS_SEND_URI, SMS_BASE_URI, PY253_SMS_VARIABLE_URI, PY253_BALANCE_GET_URI,
    PY253_SMS_PULL_MO_URI, PY253_SMS_PULL_REPORT_URI,
)
import urllib


class InternalMessage(Account):
    """
    国内短信接口
    """

    def __init__(self, account=None, password=None, uri=SMS_BASE_URI):
        super().__init__(account, password, uri)

    def send_sms(self, text, phone, sendtime: str = None, report=False, extend: int = None, uid: str = None):
        """
        用接口发短信
        """
        assert isinstance(phone, (str, list))
        assert isinstance(report, bool)
        assert uid is None or isinstance(uid, str)
        if isinstance(phone, list):
            phone = ",".join(phone)
        if sendtime is not None:
            if isinstance(sendtime, datetime.datetime):
                sendtime = sendtime.strftime("%Y%m%d%H%M%S")
        if extend is not None:
            assert 100 <= extend <= 999
        send_sms_params = {
            'msg': urllib.request.quote(text),
            'phone': phone,
            'report': "true" if report else "false",
            'sendtime': sendtime,
            'extend': extend,
            'uid': uid
        }
        params = dict(self.public_params(), **send_sms_params)
        return requests.post(self.uri + PY253_SMS_SEND_URI, json=params).json()

    def variable_sms(self, text, params, sendtime: str = None, report=False, extend: int = None, uid: str = None):
        """
        用接口发短信
        """
        assert isinstance(params, (str, list))
        assert isinstance(report, bool)
        assert uid is None or isinstance(uid, str)
        assert text.count("{$vars}") == len(params[0]) - 1
        if isinstance(params, list):
            params = ";".join(map(lambda each: ','.join(each), params))
        if sendtime is not None:
            if isinstance(sendtime, datetime.datetime):
                sendtime = sendtime.strftime("%Y%m%d%H%M%S")
        if extend is not None:
            assert 100 <= extend <= 999
        send_sms_params = {
            'msg': urllib.request.quote(text),
            'params': params,
            'report': "true" if report else "false",
            'sendtime': sendtime,
            'extend': extend,
            'uid': uid
        }
        params = dict(self.public_params(), **send_sms_params)
        return requests.post(self.uri + PY253_SMS_VARIABLE_URI, json=params).json()

    def get_user_balance(self):
        """
        取账户余额
        """
        params = self.public_params()
        return requests.post(self.uri + PY253_BALANCE_GET_URI, json=params).json()

    def pull_mo(self, count=20):
        """拉取上行明细接口"""
        assert count <= 100
        params = dict(self.public_params(), count=count)
        return requests.post(self.uri + PY253_SMS_PULL_MO_URI, json=params).json()

    def pull_report(self, count=20):
        """拉取上行状态报告接口"""
        assert count <= 100
        params = dict(self.public_params(), count=count)
        return requests.post(self.uri + PY253_SMS_PULL_REPORT_URI, json=params).json()
