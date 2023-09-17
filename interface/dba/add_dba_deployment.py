# coding=utf-8
import requests
import urllib3
from common.common_config import logger, base_url
from common.token_str import token_sec


class AddDailiDeployment(object):
    """
    资源添部署模式
    """

    def __init__(self):
        self.url = base_url + "/core/source/db/setDeployType"
        self.method = "post"

    # 参数1资源ID，参数2 代理端口
    def request(self, dbaid, core):
        header = {
            "Authorization": token_sec
        }
        json = {
            "ids": [
                dbaid
            ],
            "deployType": 1,
            "proxyPort": core,
            "isRAC": 0,
            "ipType": "",
            "localIp": ""
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url,
                               method="post",
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        return res

    # 参数1 资源ID，参数2 旁路网卡
    def request_panglu(self, dbaid, core):
        header = {
            "Authorization": token_sec
        }
        json = {
            "ids": [
                dbaid
            ],
            "deployType": 0,
            "bindCard": core,
            "isRAC": 0,
            "ipType": "",
            "localIp": ""
        }

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url,
                               method="post",
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        return res

        # 参数1 资源ID
    def request_qiaojie(self, dbaid):
        header = {
            "Authorization": token_sec
        }
        json = {
             "ids": [
                 dbaid
            ],
            "deployType": 2,
            "isRAC": 0,
            "ipType": "",
            "localIp": ""
        }

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url,
                                method="post",
                                # data=data,
                                json=json,
                                headers=header,
                                verify=False).json()
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


if __name__ == '__main__':
    res = AddDailiDeployment().request_qiaojie(2)
    print(res)
