import requests
import urllib3

from common.common_config import logger, base_url
from instance.login import Login


class LoginInterface(object):
    """
    登录接口
    """

    def __init__(self, login: Login):
        self.url = base_url + "/login"
        self.login = login
        self._response = self.request()

    def request(self):
        json_data = {
            "username": self.login.username,
            "password": self.login.password
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json_data))
        res = requests.request(url=self.url,
                               method="post",
                               json=json_data,
                               verify=False)
        return res

    @property
    def response(self):
        if "errorCode" in self._response:
            if "errorCode" == "401":
                logger.error("{}接口的用户名或密码错误".format(__name__))
        return self._response

    @property
    def status(self):
        return self._response["status"]


# if __name__ == "__main__":
#
#     log = Login()
#     log.username = "sysadmin"
#     log.password = "VwnTFygZa5O50Ij2xlh9BM9sv5/8QObKjZ5P1Rjmym0IYw3usWvUGFGyz8EhQyR5mK9VLKCkutNBSkC0QILkFMz40QyMrOCbJYpC44rZBOKq3vNt0kL9f2iUK8EcAIfPqw6RJthUAlShaS7G6FAqGY2AS1rkeD66SxSnpqIMz1UdcnlK5sq3qxt/4JavbrqxN1KB3DgbvtpiGVG8Hb1lu5Oi8iqla2CKG+Oi0iQp6Ee/TyzJ2gC1g9R1BuZu7a7TVt+xhJkTqlOOMBJ1sHjaY0zm2uh8cyDeP12IwBSzZJ91lEdK6oy/MtVnxhnR+W29v2PKH3oSUAd4vNz6CONsCw=="
#     res = LoginInterface(log).response.headers['Authorization']
#     string = res
#     target = "Bearer "
#     token = "".join(string.split(target))
#     print(token)
#     # print(res)
