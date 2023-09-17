# coding=utf-8
import pymysql
import requests
import urllib3
from common.common_config import logger, base_url
from common.token_str import token_sec
from instance.dba import Dba


class AddConnectFace(object):
    """
    资源测试连接
    """

    def __init__(self):
        self.url = base_url + "/core/source/db/testConnection"
        self.url1 = base_url + "/core/source/db/ipConnection"
        self.method = "post"

        # self._response = self.request()

    # 测试连接
    def request_dba_connect(self, dbType, host, port, username, password):
        header = {
            "Authorization": token_sec
        }
        json = {
            "host": host,
            "port": port,
            "username": username,
            "password": password,
            "dbType": dbType
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url,
                               method=self.method,
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

        # 测试连接

    def request_connect(self, ip):
        header = {
            "Authorization": token_sec
            # "Content-Type": "application/json"
        }
        json = ip

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url1,
                               method=self.method,
                               # data=data,
                               data=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

    # @property
    # def response(self):
    #     if "message" in self._response:
    #         if "message" == "数据资源名字已存在":
    #             logger.error("{}接口的用户名或密码错误".format(__name__))
    #     return self._response
    #
    # @property
    # def status(self):
    #     return self._response["status"]

    # 测试代理连接，执行语句成功返回结果。不可链接或不成功返回:False
    def request_connect_data(self, host, user, password, database, port,strsql):
        try:
            db = pymysql.connect(host=host, user=user, password=password, database=database, port=port,
                                 charset="utf8")
            # print(db)
            cursor = db.cursor()  # 使用cursor（）方法获取游标
            cursor.execute(strsql)  # 执行sql查询语句
            result = cursor.fetchall()  # 记录查询结果
            cursor.close()  # 关闭游标
            db.close()  # 关闭数据库连接
            # print(result)  # 返回查询结果
            return result
        except:
            return False


if __name__ == '__main__':
    # # 数据资源测试连接
    # host = "192.168.1.51"
    # port = "13306"
    # username = "root"
    # password = "123456"
    # dbType = "3"
    # res = AddConnectFace().request_dba_connect(dbType=dbType, host=host, port=port, username=username,
    #                                            password=password)
    # print(res)

    # 测试连通性
    # res = AddConnectFace().request_connect("192.168.1.51")
    # print(res)
    ret = AddConnectFace()
    # 连接数据库是否成功
    host = "192.168.1.80"
    user = "root"
    password = "123456"
    database = "test_rjy"
    port = 10100
    strsql = "select id from test_rjy.test"
    res = ret.request_connect_data(host=host, user=user, password=password, database=database, port=port, strsql= strsql)
    print(res)
