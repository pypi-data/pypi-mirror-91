# snowland-253-python

# py253

[![version](https://img.shields.io/pypi/v/snowland-py253.svg)](https://pypi.python.org/pypi/snowland-py253)
[![gitee](https://gitee.com/snowlandltd/snowland-253-python/badge/star.svg)](https://gitee.com/snowlandltd/snowland-253-python/stargazers)
[![download](https://img.shields.io/pypi/dm/snowland-py253.svg)](https://pypi.org/project/snowland-py253)
[![wheel](https://img.shields.io/pypi/wheel/snowland-py253.svg)](https://pypi.python.org/pypi/snowland-py253)
![status](https://img.shields.io/pypi/status/snowland-py253.svg)

#### 介绍
创蓝253接口SDK

### 使用方法

```python
import configparser
from snowland_py253.account_manage import AccountManage
from snowland_py253.internal_message import InternalMessage
cp = configparser.ConfigParser()
cp.read('../config.conf')
account = cp.get('sms', 'account')
password = cp.get('sms', 'password')
acc = InternalMessage(account=account, password=password)


# sms = acc.send_sms("【雪域网络】测试接口", "15343126139")
# print(sms)
pull = acc.pull_mo()
print(pull)
pull = acc.pull_report()
print(pull)

balance = acc.get_user_balance()
print(balance)

acc = AccountManage(account=account, password=password)
balance = acc.add_sub_account()
print(balance)

```
