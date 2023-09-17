import os

BASE_DIR = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))  # 项目根路径
CONF_DIR = os.path.join(BASE_DIR, "config")  # 配置文件路径
DATA_DIR = os.path.join(BASE_DIR, "testdata")  # 测试数据文件路径
CASE_DIR = os.path.join(BASE_DIR, "testcase")  # 测试用例文件路径
