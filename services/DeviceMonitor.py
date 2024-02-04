import os
import unittest
import time
from unittestreport import TestRunner

import requests

from bean import LogPrint, interface_address
from bean.ConfigData import ConfigData
from db import DbData
from db.Elements import Config
from devicedb import ImDeviceDbData

from services import LoginMethod
from services.DeviceAlarmService import DeviceAlarmService

# 设备监控
from services.LoginMethod import getGlobalLogin

log = LogPrint.log()


class DeviceMonitor(unittest.TestCase):

    def comm_check_status(self, deviceList, session, flag=False):
        # 如果在数据库中找到了指定设备列表则使用指定设备进行检测
        for device in deviceList:
            deviceReq = interface_address.prefixUrl + interface_address.device_list + '?' + str(
                device.device_code) + '&departmentId=0&systemType=' + str(device.type) + '&pageNumber=1&pageSize=10'
            req = requests.get(deviceReq, headers=session)
            reqJson = req.json()
            # 返回结果集中包含了该设备才进入检测
            if str(reqJson).find(device.device_code) > 0:
                devList = reqJson['data']['list']
                for dev in devList:
                    dev_code = dev['code']
                    LogPrint.log().info("开始检测设备在线：" + dev_code)
                    on_status = dev['onlineStatus']
                    assert on_status is True
                    if flag:
                        alarm_status = dev['alarmStatus']
                        assert alarm_status is True
        # 如果没有，则采用查询用电的前20个设备为基础
        if deviceList is None or deviceList.__len__ == 0:
            deviceReq = interface_address.prefixUrl + interface_address.device_list + '?departmentId=0&systemType=3&pageNumber=1&pageSize=10'
            req = requests.get(deviceReq, headers=session)
            reqJson = req.json()
            # 返回结果集中包含了该设备才进入检测，只看是否在线
            if str(reqJson).find(device.device_code) > 0:
                devList = reqJson['data']['list']
                for dev in devList:
                    dev_code = dev['code']
                    LogPrint.log().info("开始检测设备默认前10个是否在线：" + dev_code)
                    on_status = dev['onlineStatus']
                    assert on_status is True
                    if flag:
                        alarm_status = dev['alarmStatus']
                        assert alarm_status is True


    def test_checkDeviceStatus(self):
        self._testMethodDoc = '开始检测设备在线情况'
        configList = DbData.search_tab_config()
        for config in configList:
            LoginMethod.login_user(config)
            # 查询设备状态，必定是报警状态，暂停5s防止状态没有及时变更
            # time.sleep(5)
            session = getGlobalLogin()
            deviceList = DbData.search_device_by_pid(config.id)
            self.comm_check_status(deviceList, session)

    def test_device_data(self, device):
        self._testMethodDoc = '开始执行设备报警处理流程'
        config = Config()
        config.id = 3
        config.userName = 'hcds0001'
        config.pwd = 'Tpson123456'
        config.platformPrefix = 'https://cloud.sendiag.cn'
        config.status = '0'
        LoginMethod.login_user(config)
        session = getGlobalLogin()

        configData = ConfigData()
        configData.trigger = 1
        configData.randomTrigger = 2
        configData.triggerType = 1
        # configData.triggerType = 3 # 都触发
        # http://192.168.0.251:5000/device?host=192.168.0.214&port=7893&deviceId=SM20230303&deviceType=EMR1002
        msg = DeviceAlarmService().deviceAlarm(device.host, device.port, device.deviceId, device.device_type,
                                               configData)
        # 等待5秒检查设备状态必须含有报警
        time.sleep(5)
        deviceReq = interface_address.prefixUrl + interface_address.device_list + '?code=' + str(
            device.deviceId) + 'departmentId=0&systemType=3&pageNumber=1&pageSize=10'
        req = requests.get(deviceReq, headers=session)
        reqJson = req.json()
        # 返回结果集中包含了该设备才进入检测，只看是否在线
        if str(reqJson).find(device.deviceId) > 0:
            devList = reqJson['data']['list']
            for dev in devList:
                dev_code = dev['code']
                LogPrint.log().info("开始检测设备是否在线何报警状态：" + dev_code)
                on_status = dev['onlineStatus']
                assert on_status is True
                alarm_status = dev['alarmStatus']
                assert alarm_status is True
        # 报警中心的
        deviceReq = interface_address.prefixUrl + interface_address.alarm_by_code +  '?departmentId=0&pageNumber=1&pageSize=10&orderColumn=&orderType=&code='+str(device.deviceId)+'&siteName=&type=&level=1,2,3&deviceIds=&status=&result=1,0&dealUserId='
        req = requests.get(deviceReq, headers=session)
        reqJson = req.json()
        dataList = reqJson['data']['list']
        assert dataList is not None
        assert dataList.__len__ > 0
        # 处理报警数据
        alarm_id = dataList[0]['id']
        deviceReq = interface_address.prefixUrl + interface_address.alarm_deal
        data = {
            'dealDetail':'消防测试',
            'id':alarm_id,
            'status':4
        }
        req = requests.post(deviceReq, headers=session,data=data)
        reqJson = req.json()
        result = reqJson['resultCode']
        # 判断处理成功
        assert str(result) == 'SUCCESS'



    # 检查设备状态！必须传入json对象
    def check_device_status(self, dev, status):
        dev_code = dev['code']
        LogPrint.log().info("开始检测设备在线/报警：" + dev_code)
        on_status = dev['onlineStatus']
        on_status = dev['onlineStatus']
        assert on_status is True
        alarm_status = dev['alarmStatus']
        assert alarm_status is True
        fault_status = dev['faultStatus']


if __name__ == '__main__':
    s = '478984698wrwerwewe23423'
    p = '46'
    print(p.find(s))
