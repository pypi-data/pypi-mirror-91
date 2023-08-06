#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: account_manage.py
# @time: 2019/5/13 16:03
# @Software: PyCharm


__author__ = 'A.Star'

from snowland_py253.account import Account
import datetime
import requests
from snowland_py253.common import (
    ACCOUNT_BASE_URI, PY253_SUBACCOUNT_ADD_URI,
)
from pysmx.crypto import hashlib
from astartool.random import random_string


class AccountManage(Account):
    def __init__(self, account=None, password=None, uri=ACCOUNT_BASE_URI):
        super().__init__(account, password, uri)

    def add_sub_account(self,
                        product_permit_pay: str,
                        use_type=0,
                        use_desc=None,
                        name: str = None,
                        department: str = None,
                        position:str=None,
                        account_username=None,
                        account_password=None):
        """
        timestamp	是	时间戳（10位）
        signature	是	签名（小写32位md5加密）。例如signature=md5(username+password+timestamp)两边通过相同的签名进行校验
        product_permit_pay	是	需要设置子账号的扣款类型，格式为 产品id:扣款类型，比如 49:1 代表行业验证码主帐号计费，49:0代表示子账号独立计费；该子账号同时创建验证码短信和会员营销短信产品示例：'product_permit_pay'='49:0,52:0'
        use_type	是	用途分类 如：0其它,1web，2app
        use_desc	是	子账号用途（1-50字符）
        name	是	姓名（<50字符）
        department	是	部门或分部名称（<=50个字）
        position	是	职位（<=8个字）
        account_username	是	要开通的子账号名称（6-20字符）
        account_password	是	要开通的子账号密码（6-16字符）
        """

        md5 = hashlib.md5()
        username = self.access_key
        password = self.access_secret
        timestamp = str(int(datetime.datetime.now().timestamp()))
        assert len(timestamp) == 10
        md5.update((username + password + timestamp).encode())
        signature = md5.hexdigest()
        app_id, method = product_permit_pay.split(':')
        assert app_id in ('49', '52')
        assert method in ('0', '1'), "method in (0, 1)"
        assert use_type in (0, 1, 2), "use_type must in (0, 1)"
        assert 0 <= len(department) <= 50, "department < 50 words"
        data = dict(
            username=self.access_key,
            product_permit_pay=product_permit_pay,
            timestamp=timestamp,
            signature=signature,
            use_type=use_type,
            use_desc=use_desc,
            name=name,
            position=position,
            department=department,
            account_username=account_username,
            account_password=account_password)
        return requests.post(self.uri + PY253_SUBACCOUNT_ADD_URI, data=data, verify=False).json()
