# -*- coding:UTF-8 -*-
import asyncio
import datetime
import hashlib
import json
import random
import re
import time

import requests


class HandlerAlarm:

    def handlerAlarm(self, session):
        getAlarmPage = 'http://192.168.0.188:8884/self_operator/alarm/page?departmentId=0&pageNumber=1&pageSize=50&orderColumn=&orderType=&code=&siteName=&type=&level=1,2,3&status=&result=&dealUserId='
        headers = {"Cookie": "SESSION=" + str(session)}
        req = requests.get(getAlarmPage, headers=headers)
        alarmList = req.json()['data']['list']
        alarmIds = ''
        for i in range(0, alarmList.__len__() - 1):
            alarmId = alarmList[i]['id']
            alarmIds = alarmIds + str(alarmId) + ','
        # 拿到需要处理的id后，就需要调用处理按钮

        batchdeal = 'http://192.168.0.188:8884/self_operator/alarm/batch_deal'
        formdata = {
            'dealDetail': "自动处理",
            'ids': alarmIds,
            'status': '5'
        }
        req = requests.put(batchdeal, data=formdata, headers=headers)
        if req.text.find('处理') > 0:
            return '2'
        print(req.json())

        return '1'

    def handlerFault(self, session):
        getAlarmPage = 'http://10.0.0.193:8884/self_operator/fault/page?departmentId=0&pageNumber=1&pageSize=50&orderColumn=&orderType=&code=&siteName=&type=&level=&status=&dealUserId='
        headers = {"Cookie": "SESSION=" + str(session)}
        req = requests.get(getAlarmPage, headers=headers)
        faultList = req.json()['data']['list']
        faultIds = ''
        for i in range(0, faultList.__len__() - 1):
            faultId = faultList[i]['id']
            faultIds = faultIds + str(faultId) + ','
        # 拿到需要处理的id后，就需要调用处理按钮

        batchdeal = 'http://10.0.0.193:8884/self_operator/fault/batch_deal'
        formdata = {
            'dealDetail': "自动处理",
            'ids': faultIds,
            'status': '1'
        }
        req = requests.put(batchdeal, data=formdata, headers=headers)
        print(req.json())
        if req.text.find('处理') > 0:
            return '2'
        print(req.json())
        return '1'

    # 批量删除模拟器设备
    def delDeviceCenterDevice(self, k):
        req = requests.get('http://192.168.0.16:9903/v1/simulator/open/api/page?pageNumber=' + str(k) + '&pageSize=10')
        deviceLsit = req.json()['data']['list']
        ids = ''
        for i in range(deviceLsit.__len__() - 1):
            device = deviceLsit[i]
            devId = device['id']
            ids = devId + ',' + ids
        req = requests.delete('http://192.168.0.16:9903/v1/simulator/open/api/delete?ids=' + ids)
        print(req.text)

    # 修改模拟器设备数据
    def updateDeviceConfig(self):
        for i in range(1, 111):
            req = requests.get(
                'http://192.168.0.16:9903/v1/simulator/open/api/page?pageNumber=' + str(i) + '&pageSize=10')
            deviceLsit = req.json()['data']['list']
            for i in range(deviceLsit.__len__()):
                device = deviceLsit[i]
                device['period'] = 60
                device['deviceIds'] = device['id']
                device['faultRate'] = 50
                device['alarmRate'] = 50
                print(device)
                reqUpdate = requests.post('http://192.168.0.16:9903/v1/simulator/open/api/updateSimulator', json=device)
                print(reqUpdate.text)


if __name__ == '__main__':
    # HandlerAlarm().updateDeviceConfig()
    # for i in range(1, 101):
    #     print(i)
    #     HandlerAlarm().delDeviceCenterDevice(i)
    while True:
        print("开始处理故障和报警！")
        for i in range(0, 10):
            alarmInfo = HandlerAlarm().handlerAlarm('MjM2NjQyNTYtMzE1Ny00YmVlLWFjYzItOGUyZjJmODk3Nzdl')
            # faultIds = HandlerAlarm().handlerFault('MjM2NjQyNTYtMzE1Ny00YmVlLWFjYzItOGUyZjJmODk3Nzdl')
            # if faultIds == '2':
            #     print("故障和报警已经全部处理完毕，等待180s")
            #     time.sleep(180)
