#-*- coding:UTF-8 -*-

import logging
import re
import time
from datetime import datetime

from db import DbData
from db.Elements import DevicesLog
from services.LoginMethod import login_user, getGlobalLogin
from tcpConnUtils.TcpUtils import tcp_utils
import requests


# 发送报警信息且检查设备状态和通讯时间
def alarmCheck(devices, targetSession):
    print("报警设备：" + str(devices.devicesId))
    nowTimestamp = int(time.mktime(time.localtime(time.time())))
    logging.info("当前时间：" + str(time.time()))
    try:
        tcp_utils(devices.conProfix, devices.conPort, devices.alarm)
        time.sleep(5)
    except Exception as e:
        devLog = DevicesLog()
        devLog.executeLog = devices.alarm
        devLog.devicesId = devices.devicesId
        devLog.logTime = nowTimestamp  ## 日志记录时间
        devLog.result = False
        devLog.describe = "tcp链接失败，请检查！"
        DbData.insert_devices_log_time(devLog)
        return
    # 当前时间戳
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(nowTimestamp))
    nowTime = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    print("nowTime：" + str(nowTime))
    req = requests.get(devices.devicesStatusLink, cookies={'SESSION': targetSession})
    resText = req.text

    logTime = devices.searchTimeField
    result = re.search(logTime + '\D:[0-9]*', resText)
    targetTimeStamp = result.group()
    r = str(targetTimeStamp.split(":")[1])
    sf = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(r)))
    targetTime = datetime.strptime(sf, "%Y-%m-%d %H:%M:%S")
    print("targetTime" + str(targetTime))
    result = (nowTime - targetTime).seconds
    print("描述：" + str(result))
    if resText.find("报警") <= 0:
        result = None
        if "alarmStatus" in resText:
            result = re.search('alarmStatus\D:true*', resText)
        if result is not None and result.group() is  None or result is None:
            print("报警数据上报后设备状态中未查到报警信息，请检查！")
            devLog = DevicesLog()
            devLog.executeLog = devices.alarm
            devLog.devicesId = devices.devicesId
            devLog.logTime = nowTimestamp  ## 日志记录时间
            devLog.result = False
            devLog.describe = "报警数据上报后设备状态中未查到报警信息，请检查！"
            DbData.insert_devices_log_time(devLog)

            return
    elif result > int(devices.checkTime):
        print("最后通讯时间已超过规定时间，请检查！")
        devLog = DevicesLog()
        devLog.executeLog = devices.alarm
        devLog.devicesId = devices.devicesId
        devLog.logTime = nowTimestamp  ## 日志记录时间
        devLog.result = False
        devLog.describe = "最后通讯时间已超过规定时间，请检查！"
        DbData.insert_devices_log_time(devLog)
        return
    devLog = DevicesLog()
    devLog.executeLog = devices.alarm
    devLog.devicesId = devices.devicesId
    devLog.logTime = nowTimestamp  ## 日志记录时间
    devLog.result = True
    devLog.describe = "通讯正常"
    DbData.insert_devices_log_time(devLog)

    print("无论成功于否均要记录入库")


# 发送通讯信息且检查设备状态和通讯时间[3为直接查询设备最后一次通讯时间，不会发送通讯消息]
def commonCheck(devices, targetSession):
    nowTimestamp = int(time.mktime(time.localtime(time.time())))
    if devices.isAlert != '3':
        try:
            tcp_utils(devices.conProfix, devices.conPort, devices.common)
            time.sleep(5)
        except Exception as e:
            devLog = DevicesLog()
            devLog.executeLog = devices.alarm
            devLog.devicesId = devices.devicesId
            devLog.logTime = nowTimestamp  ## 日志记录时间
            devLog.result = False
            devLog.describe = "tcp链接失败，请检查！"
            DbData.insert_devices_log_time(devLog)
            return
    # 当前时间戳
    print("通讯设备：" + str(devices.devicesId))
    logging.info("当前时间：" + str(time.time()))
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(nowTimestamp))
    nowTime = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    print("nowTime：" + str(nowTime))
    req = requests.get(devices.devicesStatusLink, cookies={'SESSION': targetSession})
    resText = req.text
    logTime = devices.searchTimeField
    result = re.search(logTime + '\D:[0-9]*', resText)
    targetTimeStamp = result.group()
    r = str(targetTimeStamp.split(":")[1])
    sf = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(r)))
    targetTime = datetime.strptime(sf, "%Y-%m-%d %H:%M:%S")
    print("targetTime" + str(targetTime))
    result = (nowTime - targetTime).seconds
    if result > int(devices.checkTime):
        devLog = DevicesLog()
        devLog.executeLog = devices.alarm
        devLog.devicesId = devices.devicesId
        devLog.logTime = nowTimestamp  ## 日志记录时间
        devLog.result = False
        devLog.describe = "最后通讯时间已超过规定时间，请检查！"
        DbData.insert_devices_log_time(devLog)
        return
    devLog = DevicesLog()
    devLog.executeLog = devices.alarm
    devLog.devicesId = devices.devicesId
    devLog.logTime = nowTimestamp  ## 日志记录时间
    devLog.result = False
    devLog.describe = "通讯正常"
    DbData.insert_devices_log_time(devLog)
    print("无论成功于否均要记录入库")


class DeviceTcpService:
    def call_device_data(self):
        login_user()
        session = getGlobalLogin()
        devicesList = DbData.search_tab_devices_all()

        for devices in devicesList:
            if int(devices.status) == 1:
                if devices.isAlert == '1':
                    config = DbData.search_tab_conf_by_devices(devices.configId)
                    targetSession = session[int(config.id)]
                    alarmCheck(devices, targetSession)
                else:
                    config = DbData.search_tab_conf_by_devices(devices.configId)
                    targetSession = session[int(config.id)]
                    commonCheck(devices, targetSession)
