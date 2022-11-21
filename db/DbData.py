#-*- coding:UTF-8 -*-

import datetime
import hashlib
import logging
import re
import time
from sqlalchemy.orm import sessionmaker

from db.Elements import Devices, Config, DevicesLog
from db.base import engine

Session = sessionmaker(bind=engine)
session = Session()

def search_tab_devices_log() -> list:
    """
    :rtype: object
    """
    # 165
    ele_list = session.query(DevicesLog).all()
    return ele_list

# 配置查询
def search_tab_config() -> Config:
    """
    读取配置表中的内容，返回所有数据
    :rtype: object
    :return:
    """
    list = []
    conf_list = session.query(Config).all()
    if conf_list.__len__() >= 1:
        for key in conf_list:
            list.append(key)
    return list


'''
查询表中所有得设备
'''


def search_tab_devices_all() -> list:
    """

    :rtype: object
    """
    # 165
    ele_list = session.query(Devices).all()
    return ele_list

# 根据设备id查询数据
def search_tab_by_id_devices(devicesId: str) -> Config:
    """
    :rtype: Elements
    """
    logging.info("接受到查询请求,请求参数为: " + str(devicesId))
    result = session.query(Devices).filter_by(devicesId=devicesId).all()
    return result[0]

'''
根据条件查询表中得平台配置信息
'''


def search_tab_conf_by_devices(configId: str) -> Config:
    """
    :rtype: Elements
    """
    logging.info("接受到查询请求,请求参数为: " + str(configId))
    result = session.query(Config).filter_by(id=configId).all()
    return result[0]

def insert_devices_log_time(devicesLog:DevicesLog):
    session.add(devicesLog)
    session.commit()




if __name__ == '__main__':
    resultStr = ""
    # ele_list = search_tab_devices_log()
    # for k in ele_list:
    #     print(k.devicesId)
    #     print(k.logTime)
    #     targetTime = time.strftime("%Y-%m-%d",time.localtime(int(k.logTime)))
    #     print(is_today(targetTime))
    #     resultStr+="设备ID："+k.devicesId+" 执行时间："+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(k.logTime))) +"执行命令："+k.executeLog + " 执行结果：" +k.result +" 执行结果描述："+k.describe
    #     print(resultStr)

    t = '{"code":0,"message":null,"data":{"list":[{"id":5352,"code":"AM20220013","name":"AM20220013","lastCommunicationTime":1668567535,"onlineStatus":true,"gatewayOnlineStatus":null,"alarmStatus":true,"faultStatus":true,"hiddenStatus":false,"closedStatus":false,"model":"SMR3002-V6-TCP","pid":null,"buildingId":239,"floorId":243,"isOutdoor":false,"lat":"0.479339599609375","lng":"0.447265625","detailedAddress":"我是详细委会","geographicId":330108002,"photoId":null,"signalValue":null,"power":null,"nodeAddress":null,"nodeId":null,"alarmAndFaultAndWorkOrderInfo":null}],"total":1},"success":true,"resultCode":"SUCCESS"}'
    result = re.search('alarmStatus\D:true*', t)
    print(result.group())