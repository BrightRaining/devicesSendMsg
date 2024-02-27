import inspect
import json
import os
import unittest

import pytest
import requests
from unittestreport import TestRunner
import unittest
import time

from utils import os_file_utils


def run_test():
    suite = unittest.defaultTestLoader.discover('services', "Test_BigDeviceMonitor.py")
    timestamp = time.time()  # 获取当前时间戳
    formatted_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(timestamp))  # 将时间戳转换为格式化字符串
    print(formatted_time)  # 输出格式化后的日期时间字符串

    runner = TestRunner(suite,
                        filename=str(formatted_time) + "-report.html",
                        report_dir="report",
                        title="消防平台设备状态自动测试报告",
                        tester="device程序",
                        desc="本程序用来检查指定账号下的设备情况和指定平台设备相关流程是否存在异常；(当执行检测异常中心流程时每一次执行前默认等待5s)")
    runner.run()



# 调用顶顶机器人得方法
def dingmessage():
    ip_config = 'http://10.0.0.32:5000/reportname?name='
    resultStr = ""
    # 当前文件所在的项目路径
    project_path = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
    file_list = os.listdir(project_path + '\\' + str('report'))
    # print(file_list)
    file_name_list = ''
    for file_name in file_list:
        file_name_result = case_msg(ip_config,file_name)
        file_name_list += file_name_result


    resultStr += "#### 程序device_monitor播报运行情况" + "\n #### 所属平台：" + '消防平台' + "\n #### 执行时间：" + time.strftime(
        "%Y-%m-%d %H:%M:%S",
        time.localtime(time.time())) + '\n #### 最新一次运行结果：' +  str(
        case_msg(ip_config,file_list[file_list.__len__() - 2])) + "\n #### 历史报告执行列表描述：" + "\n" + "-------------------\n"

    resultStr += file_name_list
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
    message = {
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


def case_msg(ip_config, file_name):
    # 当前文件所在的项目路径
    project_path = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
    file_list = os.listdir(project_path + '\\' + str('report'))
    file_name_list = ''
    faild = 0
    with open(project_path + '\\' + str('report') + '\\' + str(file_name), "r",
              encoding='utf-8') as file:
        content = file.read()
        i = content.find('<span class="text-warning">')
        k = content.find('<span class="text-danger">')
        if i > 0 and k > 0:
            faild += int(content[i + 27:i + 28])
            faild += int(content[k + 26:k + 27])
    file_name_list += ip_config + str(file_name) + '  失败用例数：' + str(faild) + '\n'
    file_name_list += '\n-------------------\n'
    return file_name_list


# 第三步：执行测试
if __name__ == '__main__':
    run_test()
    # if globals().get('testFlage'):
    #     dingmessage()
    # project_path = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
    # file_list = os.listdir(project_path + '\\' + str('report'))
    # faild = 0
    # with open(project_path + '\\' + str('report') + '\\2024-02-26-14-30-04-report.html', "r",encoding='utf-8') as file:
    #     content = file.read()
    #     i = content.find('<span class="text-warning">')
    #     faild += int(content[i+27:i+28])
    #     print(int(content[i+27:i+28]))
    #     k = content.find('<span class="text-danger">')
    #     print(int(content[k+26:k+27]))
    #     faild += int(content[k+26:k+27])
    # print(faild)


