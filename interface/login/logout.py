import os

import requests
from secsmart_autotest.lib.util.ini_config_file import IniConfigFile

from business.login.login_bus import LoginBusiness
from common.common_config import base_url, logger, ic
from util.get_path import CONF_DIR


class LogoutInterface(object):
    """
    登出接口
    """

    def __init__(self):
        self.response = None
        self.url = base_url + "/auth/user/logout"
        # self.login = login
        # self._response = self.request()

    def request(self, number):
        number = number["用户名"]
        token = LoginBusiness().login(用户名=number, 密码="Admin!123456").headers['Authorization']
        headers = {
            "Authorization": token
        }
        # url = "https://192.168.1.101/auth/user/logout"
        resout = requests.request(url=self.url,
                               method="post",
                               # params=json_data,
                               headers=headers,
                               verify=False).json()
        return resout

    # @property
    # def response(self):
    #     logger.info("{}接口的返回数据为{}".format(__name__, self._response))
    #     return self._response
    #
    # @property
    # def status(self):
    #     return self._response["status"]


if __name__ == "__main__":
    res = LogoutInterface().request()
    print(res)
