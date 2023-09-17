import time
from datetime import datetime


class timeStamp():
    '''
    将当前时间转换为毫秒时间戳
    '''
    def timeStamp(self):
        time_now = datetime.now()
        # 转换后的字符类型是int类型的
        obj_temp = int(time.mktime(time_now.timetuple()) * 1000 + time_now.microsecond / 1000)
        return str(obj_temp)

#  # 测试代码
# print(timeStamp().timeStamp())
