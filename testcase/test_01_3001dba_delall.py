
from time import sleep
import allure
import pytest
from interface.dba.dba_del_interface import DbaDelInterface
from interface.dba.dba_getid_interface import DbaGetIdInterface
from interface.dba.set_modify_status import SetModifyStatus



@allure.epic("数据库防火墙")
@allure.feature("数据资源管理")
class TestDbaDelall(object):
    """
    数据资源模块，删除所有资源
    """

    @pytest.mark.smoke_dba
    @allure.title("连续删除数据库资源正常")
#   @allure.story("数据资源")
    def test_dba_delall(self):
        """
        删除所有资源
        :return:
        """
        with allure.step("#1.频繁多次删除数据资源测试"):
            dbaidlist = DbaGetIdInterface().dba_dbaid_list()
            print(dbaidlist)
            a = 0
            while a < len(dbaidlist):
                res = SetModifyStatus().request(dbaidlist[a], 0)
                sleep(3)
                DbaDelInterface().dba_del(dbaidlist[a])
                a = a + 1
        with allure.step("#2.检查是都删除成功"):
            br = DbaGetIdInterface().dba_dbaid_list()
            assert br == "没有数据资源"

