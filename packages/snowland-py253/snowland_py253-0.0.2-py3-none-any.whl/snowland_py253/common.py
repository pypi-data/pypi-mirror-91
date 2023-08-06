#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: common.py
# @time: 2019/5/13 10:35
# @Software: PyCharm


__author__ = 'A.Star'

SMS_BASE_URI = 'http://smssh1.253.com'

# 查账户信息的URI
PY253_BALANCE_GET_URI = "/msg/balance/json"

# 智能匹配模版短信接口的URI
PY253_SMS_SEND_URI = "/msg/send/json"
# 变量短信接口
PY253_SMS_VARIABLE_URI = "/msg/variable/json"
# 拉取上行明细接口
PY253_SMS_PULL_MO_URI = '/msg/pull/mo'
# 拉取状态报告接口
PY253_SMS_PULL_REPORT_URI = '/msg/pull/report'
#
ACCOUNT_BASE_URI = "https://zz.253.com"
# 子账号添加
PY253_SUBACCOUNT_ADD_URI = "/apis/subaccount/add"
# 子账号激活
PY253_SUBACCOUNT_ACTIVE_URI = '/apis/subaccount/active'
# 子账号查询
PY253_SUBACCOUNT_GET_URI = '/apis/subaccount/get'
# 子账号调拨
PY253_SUBACCOUNT_ALLOT_URI = '/apis/subaccount/allot'
# 子账号account_id查询
PY253_SUBACCOUNT_GETIDS_URI = '/apis/subaccount/getids'
# 子账号状态查询
PY253_SUBACCOUNT_GETSTATUS_URI = '/apis/subaccount/getstatus'

APP_ID_VERIFY_CODE = 49  # 行业验证码
APP_ID_MARKETING = 51  # 营销短信

# 接口功能	URL	描述
# 子账号添加	https://zz.253.com/apis/subaccount/add	通过接口添加子账号
# 子账号激活	https://zz.253.com/apis/subaccount/active	通过接口激活子账号的产品
# 子账号查询	https://zz.253.com/apis/subaccount/get	通过接口查询子账号
# 子账号调拨	https://zz.253.com/apis/subaccount/allot	通过接口对子账号进行余额分配
# 子账号account_id查询	https://zz.253.com/apis/subaccount/getids	通过接口查询账号下的子账号id
# 子账号状态查询	https://zz.253.com/apis/subaccount/getstatus	通过接口查询子账号的审核状态
# 签名模板状态推送	http://client_url	通过接口推送签名/模板的审核情况
# 添加签名	https://zz.253.com/apis/signature/signatureAdd	通过接口添加签名
# 签名列表	https://zz.253.com/apis/signature/list	通过接口查询签名
# 删除签名	https://zz.253.com/apis/signature/del	通过接口删除签名
# 添加模板	https://zz.253.com/apis/template/add	通过接口添加短信模板
# 模板列表	https://zz.253.com/apis/template/list	通过接口查询模板
# id模板单个查询	https://zz.253.com/apis/template/getSingleTemplateInfo	通过接口查询某一个模板
# 删除模板	https://zz.253.com/apis/template/del	通过接口删除模板
# 发送记录	https://zz.253.com/apis/batchlist/list	通过接口查询短信发送的审核情况
# 短信记录	https://zz.253.com/apis/sendrecord/list	通过接口查询短信发送详情
# 提交错误记录	https://zz.253.com/apis/errorstatistics/commitError	通过接口查询提交失败详情
# 发送错误记录	https://zz.253.com/apis/errorStatistics/sendError	通过接口查询发送失败详情
# 日发送统计	https://zz.253.com/apis/sendrecord/sendDay	通过接口查询日发送统计
# 月发送统计	https://zz.253.com/apis/sendrecord/sendMonth	通过接口查询月发送统计
# 查询充值记录	https://zz.253.com/apis/balance/queryBalanceLog	通过接口查询充值记录