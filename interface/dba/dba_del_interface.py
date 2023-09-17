# coding=utf-8

import requests
from common.common_config import logger, base_url
from common.token_str import token_sec


class DbaDelInterface(object):
    """
    删除数据资源
    """

    # 通过id删除数据库资源
    def dba_del(self, dbid):
        self.url = base_url + "/core/source/db/batchDelete"
        self.method = "post"

        header = {
            "Authorization": token_sec
        }
        json = {
            "ids": [
                dbid
            ]
        }
        res = requests.request(url=self.url,
                               method=self.method,
                               headers=header,
                               json=json,
                               verify=False).json()
        return res


# if __name__ == '__main__':
#     dba = DbaDelInterface().dba_del(19)
#     print(dba)
