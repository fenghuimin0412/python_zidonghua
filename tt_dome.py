# s1 = 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoie1wiaWRcIjozLFwidXNlcm5hbWVcIjpcInN5c2FkbWluXCIsXCJwYXNzd29yZFwiOm51bGwsXCJzdGF0dXNcIjpudWxsLFwidmVyaWZpY2F0aW9uQ29kZVwiOm51bGwsXCJzeXNBdXRob3JpdGllc1wiOm51bGwsXCJqd3RWZXJzaW9uXCI6NSxcImxvY2tUaW1lXCI6bnVsbH0iLCJqdGkiOiJNelprTUdRM1lUa3RZV05qTmkwME5tTTRMVGswWWpjdFkyRXhOR0UyWWpsaFpqSXgiLCJleHAiOjE2OTEyMDQxOTd9.frIFvqjBKRz3gemiBOx0hg0m_sCIkDFX73jOx4Ex9zolik49hUICpPucDsoxarhkdCNfrKDO44teIxtYFLou3TgvzNBdP54cweFdiLUW8KzUhuf86CBCZJqwilnJhIhuZdGNTjtWmZ9V8KdxnViZxgw3LyDhFw3nbz9QLBNJUCqmhEPS4aCTe71PxfD1WfY3hde9SZ-sMI62UHzba3QCsX1SmzAdxly5uks2JX1vI1QipC3DwNF8wYFcZ1suavpylKioXGR-efrHEMxy4Xi47f5BDBiGo8cpN_4Mofu7j9VBlzTZDbJnjJ_wP-RkqMkKntUE3e3UabiYDPXOmjTu8w'
# # lst_s1 = list(s1) # 将字符串转为列表
# # lst_s1.pop(0,5) # 删除下标为1的字符
# # print(''.join(lst_s1)) # hllo
#
# string = s1
# target = "Bearer "
# token = "".join(string.split(target))
# print(token)
# from business.login.login_bus import LoginBusiness
#
# LoginBusiness().login(用户名="secadmin", 密码="Admin!123456")
import json
import os
import random
import time

import pymysql
import pytest
import requests
from secsmart_autotest.lib.util.yaml_util import YamlUtil

from common.dblink.mysql_link import dbMysql
from common.token_str import token_sys
from instance import mysql
from instance.dba import Dba
from instance.mysql import Mysql
from interface.dba.dba_del_interface import DbaDelInterface
from interface.dba.dba_getid_interface import DbaGetIdInterface
from util.get_path import DATA_DIR

# import requests
# token = "Bearer eyJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoie1wiaWRcIjoyLFwidXNlcm5hbWVcIjpcInNlY2FkbWluXCIsXCJwYXNzd29yZFwiOm51bGwsXCJzdGF0dXNcIjpudWxsLFwidmVyaWZpY2F0aW9uQ29kZVwiOm51bGwsXCJzeXNBdXRob3JpdGllc1wiOm51bGwsXCJqd3RWZXJzaW9uXCI6MTMsXCJsb2NrVGltZVwiOm51bGx9IiwianRpIjoiT1RJeFpUUmhPVFl0T0dNM05TMDBNMlV3TFRrMk5EUXRPR1JrWWpjMk9EbG1OMkV5IiwiZXhwIjoxNjkxMjE5NzU0fQ.L3I7IABWhDgNcqsSZ7Xxwhp1Dsk_2a_xCKqZzk0NaqXotRqL4u7uMqXEtH_aO1PNcYygymculTrk6ew2rTzKntbULlKXjDbVtutrcZubuxu0Z15-nCXbegksS8EJZk7vkZ0JMAWHDgck53Vg8MRHXwu63BrttwLDKwQLIydhjyQPdEmS_iyH65Ng7leq6uC_3DxFtnnz3p2tzyEyamhFCutMQvBYFwm-WPXCBv9Dsrv1y5K7BdT64XaHxYp3nS87UtwCC7AThdmo5LaNOQKA8-G8YcNMnm251bXXb2EpUulKOT9T3_JOUUDH0ODoW33wDwWmxAHcxwuJ4EghFtPu8Q"
# headers = {
#     "Authorization": token
# }
# url = "https://192.168.1.101/auth/user/logout"
# res = requests.request(url=url,
#                        method="post",
#                        # params=json_data,
#                        headers=headers,
#                        verify=False).json()
# print(res)



# # 写conf.ini文件
# import configparser
# cfp = configparser.ConfigParser()
# cfp.read("./config/test.ini")
# cfp.remove_section("token")  # 移除指定selection
# cfp.add_section("token")  # 设置option的值
# cfp.set("token", "Authorization", "11111181111")  # 注意这里的selection一定要先存在！
# # cfp.remove_option("Title2", "key1")  # 移除指定selection下的option
# with open("./config/test.ini", "w+") as f:
#     cfp.write(f)



# 添加资源
# header = {
#             "Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoie1wiaWRcIjoyLFwidXNlcm5hbWVcIjpcInNlY2FkbWluXCIsXCJwYXNzd29yZFwiOm51bGwsXCJzdGF0dXNcIjpudWxsLFwidmVyaWZpY2F0aW9uQ29kZVwiOm51bGwsXCJzeXNBdXRob3JpdGllc1wiOm51bGwsXCJqd3RWZXJzaW9uXCI6MzgsXCJsb2NrVGltZVwiOm51bGx9IiwianRpIjoiT0RZNE9HSTNNamN0WlRnNU9DMDBNREZoTFdFeFptSXRPREZqTldFd056Z3hORGRqIiwiZXhwIjoxNjkxNDY0NzE3fQ.MdxIePkoGg4gb4Xm5CEoaaRzFMWWyNWX29jLNs1H62Brjo052hb3IUDoqjlXRTIAlPNAPsnY0ZbFEc4HFhN8FhrntcPntz4if3iliZiUmLl9M01Atfbrn5cJ6MOWJZPL_y48T66l5KRC0ixT6NCr1Js0GrEhl0UD4Zfoev6o8MxJXmYxAV0vIaaKFdN2fA4FeC9SG7hd4uCZMgf9FDOhnBHHjbx1x-SpHKpKo6brTmrzeuddqwmkw7tRmHP7auZOfrOgPc1Ak76nuZgf25gPYdKlHP51uCiOIG8BgLX5ECpXBKeglLTBbKN54lHNyua5-DUT6reaMqqTjLnvC3vPcQ"
#         }
#
# data = {
#     "databaseName": "123568999",
#     "databaseType":3,
#     "host": "192.168.1.11",
#     'port':"3306",
#     'dbName': "",
#     "userName": "",
#     "password": "",
#     "otherInfo": "{\"serverType\":0,\"assistedLogin\":false}",
#         }
# url = "https://192.168.1.101/core/source/db/add"
# res = requests.request(url=url,
#         method="post",
#         # data=data,
#         json=data,
#         headers=header,
#         verify=False).json()

# print(res)

#
# testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_1003_dba_add.yaml")
# test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]
# print(testdata_file)
# print(test_data)

# def open():
#     """
#     建立数据库连接
#     :return: 数据数据
#     """
#     db = pymysql.connect(host="192.168.1.101", user="root", password="123456", database="test_rjy",port="12000", charset="utf8")
#     return db
# def query1(sql):
#     """
#     不带参数查询
#     :param sql:
#     :return:
#     """
#     db = pymysql.connect(host="192.168.1.101", user="root", password="123456", database="test_rjy",port="12000", charset="utf8")
#     cursor = db.cursor()  # 使用cursor（）方法获取游标
#     cursor.execute(sql)  # 执行sql查询语句
#     result = cursor.fetchall()  # 记录查询结果
#     cursor.close()  # 关闭游标
#     db.close()  # 关闭数据库连接
#     return result  # 返回查询结果
#
#
# if __name__ == "__main__":
#     try:
#         sql2 = "select * from test_rjy.test"
#         tuple = query1(sql2)
#         all_user_info = []
#         for index in range(len(tuple)):
#             temp_dict = dict()
#             temp_dict["id"] = tuple[index][0]
#             temp_dict["name"] = tuple[index][1]
#             all_user_info.append(temp_dict)
#         print(all_user_info)
#     except:
#         print("数据读取错误！")
# def aest():
#     try:
#         db = pymysql.connect(host="192.168.1.101", user="root", password="123456", database="test_rjy", charset="utf8")
#         print(db)
#         cursor = db.cursor()  # 使用cursor（）方法获取游标
#         cursor.execute("select * from test_rjy.test")  # 执行sql查询语句
#         result = cursor.fetchall()  # 记录查询结果
#         cursor.close()  # 关闭游标
#         db.close()  # 关闭数据库连接
#         print(result)  # 返回查询结果
#     except:
#         return "连接失败"
#         print("连接失败")
#
# if __name__ == "__main__":
#     print(aest())


# db = pymysql.connect(host="192.168.1.101", user="root", password="123456", database="test_rjy", charset="utf8")
# print(db)
# cursor = db.cursor()  # 使用cursor（）方法获取游标
# cursor.execute("select * from test_rjy.test")  # 执行sql查询语句
# result = cursor.fetchall()  # 记录查询结果
# cursor.close()  # 关闭游标
# db.close()  # 关闭数据库连接
# print(result)   # 返回查询结果
# data={'databaseName': 'testMysql271'}
# dba = DbaGetIdInterface().dba_dbname_getid(data)
# print(dba)

# dbaidlist = DbaGetIdInterface().dba_dbaid_list()
# print(dbaidlist)
# a = 0
# while a < len(dbaidlist):
#     DbaDelInterface().dba_del(dbaidlist[a])
#     a = a + 1



# mysql = Mysql()
# mysql.host = "192.168.1.80"
# mysql.user = "root"
# mysql.password = "123456"
# mysql.database = "test_rjy"
# mysql.port = 10100
# conn = dbMysql(mysql)
# results = conn.query("select id from test_rjy.test")
# print(results)
# conn.close()



# try:
#     db = pymysql.connect(host="192.168.1.80", user="root", password="123456", database="test_rjy", port = 10100,charset="utf8")
#     print(db)
#     cursor = db.cursor()  # 使用cursor（）方法获取游标
#     cursor.execute("select * from test_rjy.test")  # 执行sql查询语句
#     result = cursor.fetchall()  # 记录查询结果
#     cursor.close()  # 关闭游标
#     db.close()  # 关闭数据库连接
#     print(result)  # 返回查询结果
# except:
#     # return "连接失败"
#     print("连接失败")

db = pymysql.connect(host="192.168.1.80", user="root", password="123456", database="test_rjy", port = 10100,charset="utf8")
print(db)
cursor = db.cursor()  # 使用cursor（）方法获取游标
cursor.execute("select * from test_rjy.test")  # 执行sql查询语句
result = cursor.fetchall()  # 记录查询结果
cursor.close()  # 关闭游标
db.close()  # 关闭数据库连接
print(result)  # 返回查询结果





# from common.common_config import base_url
# string1 = base_url  # 定义一个字符串
# list_str = list(string1)  # 将字符串转换为列表
# del list_str[:8]  # 删去第一个字符
# string2 = ''.join(list_str)  # 再将列表转换成字符串
# print(string2)


# fil = open('D:/autopy/smart_dom/machine15.cr', 'rb')
# print(fil.name)


# json_data = {
#             "username": "rjy",
#             "password": "shuanyi902"
#         }
# squrl = "https://192.168.1.53:8999/login"
# res_token = requests.request(url=squrl,
#                                method="post",
#                                json=json_data,
#                                verify=False).headers["authorization"]
# res_token = str(res_token).rstrip()
# print(res_token)


# # 生成5位随机数,作为名字后缀，识别授权码下载用
# random_num = random.randint(10000, 99999)
# customName = "autotest" + str(random_num)
# print(customName)


# data1 = "ddddddddddddddddddddddddddddd"
#
# with open('D:/autopy/smart_dom/output.txt', 'w') as file:
#         file.write(data1)


# def remove_chars(s, chars):
#         new_s = ""
#         for char in s:
#                 if char not in chars:
#                         new_s += char
#         return new_s
#
#
# string = "https://192.168.1.80"
# to_remove = "https://"
# result = remove_chars(string, to_remove)
# print(result)

# name = "name6666" # 理论不支持中文
# sourceId= "41"
# startTime= "2023-08-31"
# startTime1= "00:00:00"
# endTime= "2023-08-31"
# endTime1 = "23:59:00"
#
#         # 拼接URL
# a  = "https://192.168.1.80/core/baseline/geneBaseline"
# print(a)
# addurl = a+"?name="+name+"&sourceId="+sourceId+"&startTime="+startTime+"%20"+startTime1+"&endTime="+endTime+"%20"+endTime1
# print(addurl)
# print("?name=IntelligentProtection1&sourceId=41&startTime=2023-08-31%2000:00:00&endTime=2023-08-31%2023:59:00")

#
# data = {"databaseName":"testMysql2"}
# print(data["databaseName"])


# pytest.main([
#         # '-q',  # 代表 "quiet"，即安静模式，它可以将 pytest 的输出精简化，只输出测试用例的执行结果，而不会输出额外的信息，如测试用例的名称、执行时间等等
#         '-vs',  # 指定输出用例执行信息，并打印程序中的print/logging输出
#         '-m smoke_login',  # 执行用例的目录
#         '--json-report', f'--json-report-file=json_report/report.json',  # 生成json报告，并指定存放位置
#         ])
#
# with open("json_report/report.json", "r", encoding="utf-8") as f:
#     content = json.load(f)
# res = content["summary"]
# # if res["passed1"] != 0:
# #     passed = res["passed"]
# #     print(passed)
# if 'passed' in res:
#     print('name is in json_data')

# JOB_NAME = "sys.argv[1]"
# BUILD_NUMBER = "sys.argv[2]"
# GIT_BRANCH = "sys.argv[3]"
# JOB_URL = "http://192.168.1.48:8090/job/rjy_ci_auto/" + BUILD_NUMBER + "/allure/"
# passed = 0
# failed = 0
# total = 0
# with open("json_report/report.json", "r", encoding="utf-8") as f:
#     content = json.load(f)
# res = content["summary"]
# if 'passed' in res:
#     passed = res["passed"]
# if 'failed' in res:
#     failed = res["failed"]
# if 'total' in res:
#     total = res["total"]
# currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#
# inData = {
#     "timestamp": "timestamp",
#     "sign": "sign",
#     "msg_type": "text",
#     "content": {"text": f'<at user_id=\"all\">所有人</at>'},
#     "msg_type": "interactive",
#     "card": {
#         "config": {
#             "wide_screen_mode": True,
#             "enable_forward": True
#         },
#         "elements": [{
#             "tag": "div",
#             "text": {
#                 "content": "项目名称：" + JOB_NAME + "\n构建编号：第" + BUILD_NUMBER + "次构建\n运行时间：" + currenttime + "\n分支:" + GIT_BRANCH + "\n通过用例数:" + str(
#                     passed) + "\n失败用例数:" + str(failed) + "\n本次运行用例总数:" + str(total),
#                 "tag": "lark_md"
#             }
#         }, {
#             "actions": [{
#                 "tag": "button",
#                 "text": {
#                     "content": "查看报告",
#                     "tag": "lark_md"
#                 },
#                 "url": JOB_URL,
#                 "type": "default",
#                 "value": {}
#             }],
#             "tag": "action"
#         }
#         ],
#         "header": {
#             "title": {
#                 # "content": JOB_NAME + " 构建报告",
#                 "content": "数安易CI环境每日构建报告",
#                 "tag": "plain_text",
#             }
#         }
#     }
# }
# inData1 = {
#     "timestamp": "timestamp",
#     "sign": "sign",
#     "msg_type": "text",
#     "content": {"text": f'<at user_id=\"all\">所有人</at>'}
# }
# webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/3045e132-0b88-4977-a57c-dd02b17ab23b"
# # @所有人发送信息
#
#
# resp = requests.request("POST",webhook, headers={"Content-Type": 'application/json'}, json=inData)
# # resp = requests.request("POST",webhook, headers={"Content-Type": 'application/json'}, json=inData1)
# print(resp.json())
