import configparser
import os

from secsmart_autotest.lib.util.ini_config_file import IniConfigFile

from util.get_path import CONF_DIR


class ConfWrite(object):
    """
    将Authorization写入conf.ini
    """

    def writeToINI(self, Authorization):
        cfp = configparser.ConfigParser()
        ic = IniConfigFile(os.path.join(CONF_DIR, "conf.ini"))
        ic.write("token", "Authorization",Authorization)

    def remove_chars( s=None, chars=None):
        new_s = ""
        for char in s:
            if char not in chars:
                new_s += char
        return new_s

if __name__ == '__main__':
    string = "https://192.168.1.80"
    to_remove = "https://"
    result = ConfWrite.remove_chars(string, to_remove)
    print(result)