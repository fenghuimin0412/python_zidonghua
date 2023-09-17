import os
from secsmart_autotest.lib.log import logger
from secsmart_autotest.lib.util.ini_config_file import IniConfigFile
from util.get_path import CONF_DIR


ic = IniConfigFile(os.path.join(CONF_DIR, "conf.ini"))
log_level = ic.read("log", "level").upper()
logger.setLevel(log_level)
base_url = ic.read("env", "base_url")
token = ic.read("token", "authorization")

string1 = base_url  # 定义一个字符串
list_str = list(string1)  # 将字符串转换为列表
del list_str[:8]  # 删去第一个字符
string2 = ''.join(list_str)  # 再将列表转换成字符串
daili_url = string2





