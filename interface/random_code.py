import requests
import urllib3

from common.common_config import base_url


class RandomInfoInterface(object):
    """
    随机码接口
    """

    def __init__(self):
        self.url = base_url + "/user/random_code"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._response = requests.request(url=self.url,
                                          method="get",
                                          verify=False).json()

    @property
    def response(self):
        return self._response

    @property
    def random_id(self):
        return self._response["data"]["randomId"]

    @property
    def random_code(self):
        return self._response["data"]["randomCode"]


if __name__ == "__main__":
    rd = RandomInfoInterface()
    print(rd.random_id, rd.random_code)
