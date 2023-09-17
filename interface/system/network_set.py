# coding=utf-8
import requests
import urllib3
from common.common_config import logger, base_url
from common.token_str import token_sys


class NetworkSet(object):
    """
    网卡设置
    """

    def __init__(self):
        self.url1 = base_url + "/core/network/interface/bridge/create"
        self.url2 = base_url + "/core/network/interface/bridge/remove"
        self.url4 = base_url + "/core/network/interface/route/config"
        # 查询
        self.url3 = base_url + "/core/network/interface/netcard/find"
        self.method = "post"

    # 添加桥接网卡配置
    def request_add_qj(self, enp1, enp2):
        header = {
            "Authorization": token_sys
        }
        json = {
            "from": enp1,
            "to": enp2
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url1,
                               method="post",
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        return res

    # 添加桥接网卡配置
    def request_rem_qj(self, enp1, enp2):
        header = {
            "Authorization": token_sys
        }
        json = {
            "from": enp1,
            "to": enp2,
            "mode": 2
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url2,
                               method="post",
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        return res

    # 获取网卡ip
    def request_get_ip(self, network_name):
        header = {
            "Authorization": token_sys
        }
        # json = {}
        res = requests.request(url=self.url3,
                               method="post",
                               # data=data,
                               # json = json,
                               headers=header,
                               verify=False).json()
        # res = res["data"]
        network_list = res["data"]["netCards"]
        a = 0
        while a < len(network_list):
            if network_list[a]["name"] == network_name:
                if network_list[a]["ipv4List"] != None:
                    network_list[a]["ipv4List"]
                    ip = network_list[a]["ipv4List"]
                    return ip
            a = a + 1
        return ""

    # 编辑网卡enp3,ip_net:ip/掩码，举例：192.168.1.2/24
    def request_set_network(self, enp3, ip_net):
        header = {
            "Authorization": token_sys
        }

        json = {
            "name": enp3,
            "ipv4": [
                {
                    "old": "",
                    "new": ip_net
                }
            ],
            "ipv6": "",
            "oldIpv6": "",
            "gateway": ""
        }

        old = self.request_get_ip(enp3)
        print(old)
        if len(old) == 1 :
            json = {
                "name": enp3,
                "ipv4": [
                    {
                        "old": old[0],
                        "new": ip_net
                    }
                ],
                "ipv6": "",
                "oldIpv6": "",
                "gateway": ""
            }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url4,
                               method="post",
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        return res


if __name__ == '__main__':
    network_list = NetworkSet().request_set_network("br-p12s0-p13s0", "192.168.2.81/24")
    print(network_list)
    # network_list = NetworkSet().request_get_ip("br-p12s0-p13s0")
    # print(network_list)
    # res = network_list["data"]["netCards"][0]
    # res1 = network_list["data"]["netCards"][1]
    #
    # print(network_list)
    # print(res1)
