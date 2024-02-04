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

# 调用顶顶机器人得方法
def dingmessage():
    resultStr = ""
    ele_list = DbData.search_tab_devices_log()
    for k in ele_list:
        print(k.devicesId)
        devices = DbData.search_tab_by_id_devices(k.devicesId)
        config = DbData.search_tab_conf_by_devices(devices.configId)
        # 查询平台类型使消息容易查看
        platformType = ""
        if int(config.platformType) == 1 :
            platformType = "消防平台"
        elif int(config.platformType) ==2 :
            platformType = "数字电力"
        else:
            platformType = "其他"
        print(k.logTime)
        # 判断是否为当天得数据
        targetTime = time.strftime("%Y-%m-%d", time.localtime(int(k.logTime)))
        print()
        flag = is_today(targetTime)
        resultStr = ""
        if flag:
            resultStr += "#### 设备ID：" + k.devicesId +"\n #### 所属平台："+platformType+ "\n #### 执行时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                int(k.logTime))) + "\n #### 执行命令：" + k.executeLog + "\n #### 执行结果：" + k.result + "#### 执行结果描述：" + k.describe +"\n"+"-------------------\n"
        if resultStr is None or resultStr == "":
            resultStr = "\n #### 今日暂无数据产生"

    # 请求的URL，WebHook地址
    webhook = f"https://oapi.dingtalk.com/robot/send?access_token=cf529eebb45c09fe11cbc7fdbed4b773d9893d76a262df30096bf047f15d254b"
    # 构建请求头部
    header = {"Content-Type": "application/json", "Charset": "UTF-8"}
    # message = {
    #     "msgtype": "text",
    #     "text": {"content": "监控设备,"},
    #     "at": {
    #         # @ 所有人
    #         "isAtAll": False
    #     }
    # }
    message ={
        "msgtype": "markdown",
        "markdown": {
            "title": "监控设备",
            "text": resultStr
        },
        "at": {
            # "atMobiles": [
            #     "150XXXXXXXX"
            # ],
            # "atUserIds": [
            #     "user123"
            # ],
            "isAtAll": False
        }
    }
    message_json = json.dumps(message)
    info = requests.post(url=webhook, data=message_json, headers=header, verify=False)  # 打印返回的结果
    print(info.text)



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
    # 获取当前文件所在目录
    cur_path = os.path.dirname(os.path.abspath(__file__))
    # 用例路径
    test_dir = os.path.join(cur_path, 'services')
    # 报告路径
    result_dir = os.path.join(cur_path, 'report2/')

    # 报告路径
    report_dir = result_dir
    now = time.strftime("%Y%m%d-%H_%M_%S")
    suit_tests = creatsuite()
    # 执行并自动生成测试报告
    runner = TestRunner(suit_tests,
                        filename='应用安装查询' + now + 'report.html',
                        report_dir=report_dir,
                        title='应用安装查询测试报告',
                        tester="张张",
                        desc='应用安装查询自动化测试')
    runner.run()

    # DeviceTcpService().call_device_data()
    # dingmessage()

    s = [8,9.5,10.2,8.4,9.7,10.3,10.3,8.7,8.8,9.8,9.3,10.9,8,9.3,8]
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
