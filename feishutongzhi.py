#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys
import requests
import time
import json

from interface.system.empower import Empower

JOB_NAME = sys.argv[1]
BUILD_NUMBER = sys.argv[2]
GIT_BRANCH = sys.argv[3]

# JOB_NAME = "sys.argv[1]"
# BUILD_NUMBER = "sys.argv[2]"
# GIT_BRANCH = "sys.argv[3]"
JOB_URL = "http://192.168.1.48:8090/job/rjy_ci_auto/" + BUILD_NUMBER + "/allure/"
# 读取json测试报告结果
passed = 0
failed = 0
total = 0
# 获取版本号
lic = Empower().request_find_licensestr()

with open("json_report/report.json", "r", encoding="utf-8") as f:
    content = json.load(f)
res = content["summary"]
if 'passed' in res:
    passed = res["passed"]
if 'failed' in res:
    failed = res["failed"]
if 'total' in res:
    total = res["total"]

currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
url = 'https://open.feishu.cn/open-apis/bot/v2/hook/3045e132-0b88-4977-a57c-dd02b17ab23b'
method = 'post'
headers = {
    'Content-Type': 'application/json'
}
json = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True,
            "enable_forward": True
        },
        "elements": [{
            "tag": "div",
            "text": {
                "content": "项目名称：" + JOB_NAME + "\n构建编号：第" + BUILD_NUMBER + "次构建\n运行版本："+lic+"\n运行时间：" + currenttime + "\n分支:" + GIT_BRANCH + "\n通过用例数:" + str(
                    passed) + "\n失败用例数:" + str(failed) + "\n本次运行用例总数:" + str(total),
                "tag": "lark_md"
            }
        }, {
            "actions": [{
                "tag": "button",
                "text": {
                    "content": "查看报告",
                    "tag": "lark_md"
                },
                "url": JOB_URL,
                "type": "default",
                "value": {}
            }],
            "tag": "action"
        }],
        "header": {
            "title": {
                # "content": JOB_NAME + " 构建报告",
                "content": "数安易CI环境每日构建报告",
                "tag": "plain_text"
            }
        }
    }
}
requests.request(method=method, url=url, headers=headers, json=json)
inData = {
    "timestamp": "timestamp",
    "sign": "sign",
    "msg_type": "text",
    "content": {"text": f'<at user_id=\"all\">所有人</at>'}
}
requests.request(method=method, url=url, headers=headers, json=inData)
