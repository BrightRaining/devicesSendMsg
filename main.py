#-*- coding:UTF-8 -*-

# python 3.8
import datetime
import json
# 加签
import time

import requests

from db import DbData

import os
import unittest
import time
from unittestreport import TestRunner



def is_today(target_date):
    """
    Detects if the date is current date
    :param target_date:
    :return: Boolean
    """
    # Get the year, month and day
    c_year = datetime.datetime.now().year
    c_month = datetime.datetime.now().month
    c_day = datetime.datetime.now().day

    # Disassemble the date
    date_list = target_date.split(" ")[0].split("-")
    print(date_list)
    t_year = int(date_list[0])
    t_month = int(date_list[1])
    t_day = int(date_list[2])

    final = False
    if c_year == t_year and c_month == t_month and c_day == t_day:
        final = True
    print(final)
    return final



def creatsuite():
    # 创建测试套件
    testunit = unittest.TestSuite()
    # 定义测试文件查找的目录
    case_dir = test_dir
    # 定义 discover 方法的参数（测试用例都以test开头命名）
    suit_tests = unittest.defaultTestLoader.discover(case_dir, pattern='Device*.py', top_level_dir=None)
    # discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suite in suit_tests:
        for test_case in test_suite:
            # 将测试用例添加到测试套件中
            testunit.addTests(test_case)
            print(testunit)
    return testunit


if __name__ == "__main__":


    # DeviceTcpService().call_device_data()
    # dingmessage()

    s = [9.6,9.3,9.6,9.6,9.1,8,10,9.4,9.2,8.8,]
    num = 0
    for i in s:
        num += i
    print(num / s.__len__())
    print(s.__len__())


# if __name__ == '__main__':
#     DeviceTcpService().call_device_data()
#     # t = 'logTime:1667288201'
#     # s = t.split(":")
#     # print(s[1])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
