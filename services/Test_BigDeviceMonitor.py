import unittest
import time

import requests

from bean import LogPrint, interface_address
from bean.ConfigData import ConfigData
from db import DbData

from services import LoginMethod
from services.CheckPoint import CheckPoint
from services.DeviceAlarmService import DeviceAlarmService

# 设备监控
from services.LoginMethod import getGlobalLogin
from utils.Run_Case_Monitor import listenFunc

log = LogPrint.log()


class DeviceMonitor(CheckPoint):


    def comm_check_status(self, config,deviceList, session, flag=False):
        """
        设备状态的检验都可以在这里写上
        :param deviceList:
        :param session:
        :param flag: 是否检查当前设备处于报警状态，默认不检查
        :return:
        """
        test_flag = True
        # 如果在数据库中找到了指定设备列表则使用指定设备进行检测
        for device in deviceList:
            deviceReq = config.platformPrefix + interface_address.device_list + '?' + str(
                device.device_id) + '&departmentId=0&systemType=' + str(device.type) + '&pageNumber=1&pageSize='+str(config.page_size)
            req = requests.get(deviceReq, headers=session)
            reqJson = req.json()
            # 返回结果集中包含了该设备才进入检测
            if str(reqJson).find(device.device_id) > 0:
                devList = reqJson['data']['list']
                for dev in devList:
                    dev_code = dev['code']
                    LogPrint.log().info("开始检测设备在线：" + dev_code)
                    print("开始检查指定设备在线情况：" + dev_code)
                    try:
                        on_status = dev['onlineStatus']
                        assert on_status is True
                        if flag:
                            alarm_status = dev['alarmStatus']
                            assert alarm_status is True
                    except AssertionError as e:
                        print("判断失败！设备状态有错误应为在线，请检查！" + dev_code + " " + str(e))
                        test_flag = False

        # 如果没有，则采用查询用电的前20个设备为基础
        if deviceList is None or deviceList.__len__() == 0:
            deviceReq = config.platformPrefix + interface_address.device_list + '?departmentId=0&deviceType='+str(config.device_type)+'&pageNumber=1&pageSize='+str(config.page_size)
            req = requests.get(deviceReq, headers=session)
            reqJson = req.json()
            # 返回结果集中包含了该设备才进入检测，只看是否在线
            devList = reqJson['data']['list']
            for dev in devList:
                dev_code = dev['code']
                LogPrint.log().info("开始检测设备默认前10个是否在线：" + dev_code)
                print("因未指定设备故开始检查前"+str(config.page_size)+"个设备在线情况：" + dev_code)
                try:
                    on_status = dev['onlineStatus']
                    assert on_status is True
                    if flag:
                        alarm_status = dev['alarmStatus']
                        assert alarm_status is True
                except AssertionError as e:
                    print("判断失败！设备状态有错误应为在线，请检查！" + dev_code + " " + str(e))
                    test_flag = False
        self.assertTrue(test_flag)

    @listenFunc
    def test_checkDeviceStatus(self):
        """
        此方法只做在线统计
        :return:
        """
        LogPrint.log().info("开始执行检测设备在线情况函数")
        self._testMethodDoc = '开始检测设备在线情况'
        configList = DbData.search_tab_config()
        for config in configList:
            # 状态是0，直接返回不执行
            if config.status == '0' or config.status == 0:
                continue
            LoginMethod.login_user(config)
            print("登录地址/账号/密码："+ str(config.platformPrefix) + " "+ str(config.userName) + " "+ str(config.pwd))
            # 查询设备状态，必定是报警状态，暂停5s防止状态没有及时变更
            # time.sleep(5)
            session = getGlobalLogin()
            # 从数据库中找关联数据，没有的话就默认采用分页数据
            deviceList = DbData.search_device_by_pid(config.id)
            self.comm_check_status(config, deviceList, session)

    def test_device_data(self):
        """
        触发报警的时候，必须要有设备和账号信息的限制
        :param device: 设备信息
        :param config: 账号信息
        :return:
        """
        LogPrint.log().info("开始执行检测设备报警处理流程情况函数")
        self._testMethodDoc = '开始执行设备报警处理流程'
        configList = DbData.search_tab_config()
        flage = True
        for config in configList:
            # 状态是0，直接返回不执行
            if config.status == '0' or config.status == 0:
                continue
            # config = Config()
            # config.id = 3
            # config.userName = 'hcds0001'
            # config.pwd = 'Tpson123456'
            # config.platformPrefix = 'https://cloud.sendiag.cn'
            # config.status = '0'
            LoginMethod.login_user(config)
            session = getGlobalLogin()
            print("登录地址/账号/密码："+ str(config.platformPrefix) + " "+ str(config.userName) + " "+ str(config.pwd))
            configData = ConfigData()
            configData.trigger = 1
            configData.randomTrigger = 2
            configData.triggerType = 1
            device_list = DbData.search_device_by_pid(config.id)
            for device in device_list:
                # configData.triggerType = 3 # 都触发
                # http://192.168.0.251:5000/device?host=192.168.0.214&port=7893&deviceId=SM20230303&deviceType=EMR1002
                # 触发报警
                msg = DeviceAlarmService().deviceAlarm(device.host, device.port, device.device_id, device.device_type,
                                                       configData)
                # 等待5秒检查设备状态必须含有报警
                time.sleep(5)
                deviceReq = config.platformPrefix + interface_address.device_list + '?code=' + str(
                    device.device_id) + '&departmentId=0&deviceType='+str(config.device_type)+'&pageNumber=1&pageSize='+str(config.page_size)
                req = requests.get(deviceReq, headers=session)
                reqJson = req.json()
                # 返回结果集中包含了该设备才进入检测，只看是否在线
                if str(reqJson).find(device.device_id) > 0:
                    devList = reqJson['data']['list']
                    for dev in devList:
                        dev_code = dev['code']
                        print("开始检测设备是否在线何报警状态："+ dev_code)
                        try:
                            on_status = dev['onlineStatus']
                            self.assertTrue(on_status)
                            alarm_status = dev['alarmStatus']
                            self.assertTrue(alarm_status)
                        except AssertionError as e:
                            timestamp = time.time()  # 获取当前时间戳
                            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                           time.localtime(timestamp))  # 将时间戳转换为格式化字符串
                            print("判断失败！设备状态有错误应为在线/报警，请检查！"+dev_code + " "+str(e) + " "+str(formatted_time))
                            flage = False

                # 报警中心的查询
                deviceReq = config.platformPrefix + interface_address.alarm_by_code + '?departmentId=0&pageNumber=1&pageSize=10&orderColumn=&orderType=&code=' + str(
                    device.device_id) + '&siteName=&type=&level=1,2,3&deviceIds=&status=&result=1,0&dealUserId='
                req = requests.get(deviceReq, headers=session)
                reqJson = req.json()
                dataList = reqJson['data']['list']
                try:
                    self.assertIsNotNone(dataList)
                    self.assertTrue(dataList.__len__() > 0)
                except AssertionError as e:
                    timestamp = time.time()  # 获取当前时间戳
                    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                   time.localtime(timestamp))  # 将时间戳转换为格式化字符串
                    print("判断失败！设备触发报警后报警中心查无数据，请检查！" + device.device_id + " " + str(e) + ' '+ formatted_time)
                    flage = False

                alarm_id = ''
                # 处理报警数据
                for data in dataList:
                    alarm_id = alarm_id + str(data['id']) + ','
                deviceReq = config.platformPrefix + interface_address.alarm_deal
                data = {
                    'dealDetail': '自动处理消防测试',
                    'ids': alarm_id[0:alarm_id.__len__()-1],
                    'status': 4
                }
                print("开始执行设备处理报警流程,处理的报警ids："  + str(alarm_id[0:alarm_id.__len__()-1]))
                req = requests.put(deviceReq, headers=session, data=data)
                reqJson = req.json()
                result = reqJson['resultCode']
                try:
                    # 判断处理成功
                    self.assertTrue(str(result) == 'SUCCESS')
                except AssertionError as e:
                    timestamp = time.time()  # 获取当前时间戳
                    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                   time.localtime(timestamp))  # 将时间戳转换为格式化字符串
                    print("判断失败！报警中心批量处理报警失败，请检查！" + device.device_id + " " + str(e) + ' '+ str(formatted_time))
                    flage = False
                print("=================！！！分隔符！！！=======================")
            # 如果没有，则采用查询用电的前10个设备为基础
            if device_list is None or device_list.__len__() == 0:
                print("报警处理流程，您必须指定账号和设备！否则默认通过！")
        self.assertTrue(flage)



    # 检查设备状态！必须传入json对象
    def check_device_status(self, dev, status):
        dev_code = dev['code']
        LogPrint.log().info("开始检测设备在线/报警：" + dev_code)
        on_status = dev['onlineStatus']
        assert on_status is True
        alarm_status = dev['alarmStatus']
        assert alarm_status is True
        fault_status = dev['faultStatus']


if __name__ == '__main__':
    import time
    timestamp = time.time()  # 获取当前时间戳
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))  # 将时间戳转换为格式化字符串
    print(formatted_time)  # 输出格式化后的日期时间字符串
