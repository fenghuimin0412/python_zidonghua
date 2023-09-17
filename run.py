import os
import pytest
from util.get_path import CASE_DIR

# 原始的脚本
# if __name__ == "__main__":
#     g = os.walk(CASE_DIR)
#     case_list = [file_list for path, dir_list, file_list in g]
#     print(case_list)
#     case_list[0].remove("_11111_init__.py")去掉1111
#     print(case_list)
#     for case in case_list[0]:
#         os.system(r"pytest --reruns 5 -s {}".format(os.path.join(CASE_DIR, case)))
#     # 执行测试用例生成json测试结果数据
#     os.system(r"pytest --alluredir ./report --clean-alluredir")
#     os.system(r"allure serve report")

# # 执行所有测试用例
# if __name__ == "__main__":
#     os.system(r"pytest --alluredir ./report --clean-alluredir")
#     # --clean-alluredir 为每次清理报告记录。如需要保留历史记录可删除掉，如下
#     os.system(r"pytest --alluredir ./report ")
#     os.system(r"allure serve report -p 15566")

# 执行某一个标签的测试用例
if __name__ == '__main__':
    # 标签名为smoke_rules，且不需要加引号
    os.system(r"/usr/local/python3.10/python/bin/pytest  --alluredir=./report --clean-alluredir --json-report --json-report-file=json_report/report.json")
    # os.system(r"/usr/local/python3.10/python/bin/pytest -m smoke_login --alluredir=./report --clean-alluredir --json-report --json-report-file=json_report/report.json")
    # --clean-alluredir 为每次清理报告记录。如需要保留历史记录可删除掉，如下
    # os.system(r"pytest -m smoke_jixian --alluredir=./report --clean-alluredir --json-report --json-report-file=json_report/report.json")
    # os.system(r"allure serve report -p 15566")

# # 执行某一个测试用例
# if __name__ == '__main__':
#     # 标签名为smoke_rules，且不需要加引号
#     os.system(r"pytest ./testcase/test_01_1001_login.py --alluredir=./report --clean-alluredir")
#     # --clean-alluredir 为每次清理报告记录。如需要保留历史记录可删除掉，如下
#     # os.system(r"pytest -m smoke_rules --alluredir=./report")
#     os.system(r"allure serve report -p 15566")

# 注意一定要将被测系统时间同步一下。time.windows.com
