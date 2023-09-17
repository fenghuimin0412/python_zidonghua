# coding=utf-8
import requests
import urllib3
from common.common_config import logger, base_url
from common.token_str import token_sec


class SetModifyStatus(object):
    """
    设置数据资源状态
    """

    def __init__(self):
        self.url = base_url + "/core/source/db/modifyStatus"
        self.method = "post"

        # self._response = self.request()

    def request(self, dbaid,status):
        header = {
            "Authorization": token_sec
        }
        json = {
            "id": dbaid,
            "status": status
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url,
                               method="post",
                               # data=data,
                               json=json,
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

if __name__ == '__main__':
    res = SetModifyStatus().request(12,0)
    print(res)
