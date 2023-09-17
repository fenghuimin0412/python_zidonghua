import os
from time import sleep

import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from business.dba.add_dba_business import AddDbaBusiness
from common.common_config import base_url
from instance import dba
from instance.audlog import Audlog
from interface.auditlog_query import AuditLogInterface
from interface.dba.add_dba_connect import AddConnectFace
from interface.dba.add_dba_deployment import AddDailiDeployment
from interface.dba.dba_getid_interface import DbaGetIdInterface
from interface.dba.set_modify_status import SetModifyStatus
from interface.rule.Intelligent_protection_set import IntelligentProtectionFace
from interface.rule.rule_conf import RuleConfFace
from interface.rule.rule_set import RuleAddInterface
from interface.rule.strategy_set import StrategySetFace
from util.conf_w import ConfWrite
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("安全策略")
class TestRuleCof(object):
    """
    策略应用
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_02_5007_rule_cof.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]
    @pytest.mark.smoke_jixian
    @pytest.mark.parametrize("data", test_data)
    @allure.title("策略配置_记录结果集测试")
    # @allure.story("")
    def test_01(self, data):
        """
        策略应用
        """
        # 设置策略：应用虚拟补丁策略，为了更好的检索日志
        with allure.step("#1.为数据资源应用策略：虚拟补丁、记录结果集、记录日志"):
            res = RuleConfFace().request_result_conf(data["sourceName"])
            assert res["data"] == "success"
        # 测试资源执行：SELECT table_name FROM INFORMATION_SCHEMA.TABLES
        with allure.step("#2.访问代理资源，执行：SELECT table_name FROM INFORMATION_SCHEMA.TABLES"):
            ret = AddConnectFace()
            daili_url = ConfWrite.remove_chars(base_url, "https://")
            res = ret.request_connect_data(host=daili_url, user=data["user"], password=data["password"],
                                           database=data["database"], port=data["port"], strsql=data["strsql"])
            assert res != False
        with allure.step("#3.获取最新10秒内日志，检索到一条操作为：select id from test_rjy.test的审计日志，记录了结果集"):
            aud = Audlog()
            aud.sqlRequestContent = data["strsql"]
            res = AuditLogInterface().request(aud)
            # 判断12秒内生成一条数据并且sql语句为select id from test_rjy.test
            a = 0
            while a < 12:
                sleep(1)
                res1 = res = AuditLogInterface().request(aud)["data"]["data"]
                if len(res1) != 0:
                    # print(res1)
                    res = res1[0]["sqlResultContent"]
                    break
                a = a+1
            # 检索该字段有值，就记录了结果集
            # print(res)
            assert res != ""
