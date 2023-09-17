# coding=utf-8
import random
from time import sleep
import requests
import urllib3
from common.common_config import logger, base_url
from common.token_str import token_sys


class Empower(object):
    """
    自动授权
    """

    def __init__(self):
        self.url1 = base_url + "/auth/license/getServerInfo"
        self.url2 = base_url + "/auth/license/install"
        # 查询授权状态
        self.url3 = base_url + "/auth/license/getProductInfo"
        self.method2 = "post"
        self.method1 = "get"

    # 授权
    # noinspection PyUnreachableCode
    def request_install(self):
        # 获取机器码

        header = {
            "Authorization": token_sys
        }

        res = requests.request(url=self.url1,
                               method=self.method1,
                               # data=data,
                               # json=json,
                               headers=header,
                               verify=False).text
        # 获取授权系统token

        # 生成5位随机数,作为名字后缀，识别授权码下载用
        random_num = random.randint(10000, 99999)
        customName = "autotest" + str(random_num)
        json_data = {
            "username": "rjy",
            "password": "shuanyi902"
        }
        squrl = "https://192.168.1.53:8999/login"
        res_token = requests.request(url=squrl,
                                     method="post",
                                     json=json_data,
                                     verify=False).headers["authorization"]
        res_token = str(res_token).rstrip()
        print(res_token)

        # 使用机器码在授权系统授权
        url = "https://192.168.1.53:8999/platform/licence/addLicence"
        header = {
            "Authorization": res_token
        }
        # files = {"machineCodeFile": open('D:/autopy/smart_dom/machine15.cr', 'rb')}
        files = {"machineCodeFile": res}
        data = {
            "customName": customName,
            "productType": 1,
            "authType": 0,
            "effectiveRange": "2023-08-25 14:45:26~2024-09-25 14:45:26",
            "dataSourceCount": 20
        }
        res1 = requests.request(url=url,
                                method="post",
                                data=data,
                                # data=data,
                                files=files,
                                headers=header,
                                verify=False)
        # return res1.json()
        sleep(5)
        # 下载授权证书
        # 查询授权信息ID
        urlf = "https://192.168.1.53:8999/platform/licence/searchLicence"
        headers = {
            "Authorization": res_token
        }
        data = {
            "pageNo": 1,
            "pageSize": 10
        }
        resf = requests.request(url=urlf,
                                method="post",
                                json=data,
                                # data=data,
                                headers=headers,
                                verify=False).json()["data"]["dtoList"]
        dataid = 0
        # customName = "autotest49288"
        for a in resf:
            if a["customName"] == customName:
                # #     print(a["customName"])
                dataid = a["id"]
        # return dataid
        # print(dataid)

        # 通过ID下载授权文件
        urlx = "https://192.168.1.53:8999/platform/licence/downloadLicense"
        header = {
            "Authorization": res_token,
            # "content-type": "application/x-download;charset=utf-8"
        }
        data = {
            "id": dataid
        }
        response = requests.request(url=urlx,
                                    method="post",
                                    json=data,
                                    # data=data,
                                    headers=header,
                                    verify=False).content
        # print(response)
        # td = response.text
        # print(response)
        # with open('D:/autopy/smart_dom/output.lic', 'ab') as file:
        #     file.write(response)
        # file.close()
        # 给被测系统授权
        header = {
            "Authorization": token_sys

        }
        kwargs = {"file": response}
        res = requests.request(url=self.url2,
                               method="post",
                               # data = data,
                               files={"file": response},
                               headers=header,
                               verify=False
                               )
        return res.json()

    # 检查是否授权
    def request_find_license(self):
        header = {
            "Authorization": token_sys
        }
        # url5 = "https://192.168.1.102/auth/license/getProductInfo"
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url3,
                               method="post",
                               # data=data,
                               # json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        # res["data"]
        return res["data"]["hasAuth"]

    # 获取授权信息
    def request_find_licensestr(self):
        header = {
            "Authorization": token_sys
        }
        # url5 = "https://192.168.1.102/auth/license/getProductInfo"
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url3,
                               method="post",
                               # data=data,
                               # json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        # res["data"]
        return res["data"]


if __name__ == '__main__':
    # network_list = Empower().request_install()
    # print(network_list)

    # # 查询授权
    # lic = Empower().request_find_license()
    # print(lic)

    # 获取授权信息
    lic = Empower().request_find_licensestr()
    print(lic["productVersion"])
