# -*- coding:UTF-8 -*-

import datetime
import hashlib
import logging
import re
import time
from sqlalchemy.orm import sessionmaker

from db.Elements import Config, Device
from db.base import engine

Session = sessionmaker(bind=engine)
session = Session()


# 配置查询
def search_tab_config() -> Config:
    """
    读取配置表中的内容，返回所   有数据
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
    ele_list = session.query(Device).all()
    return ele_list


# 根据设备id查询数据
def search_tab_by_id_devices(devicesId: str) -> Config:
    """
    :rtype: Elements
    """
    logging.info("接受到查询请求,请求参数为: " + str(devicesId))
    result = session.query(Device).filter_by(devicesId=devicesId).all()
    return result[0]

def search_tab_by_type_devices(deviceType: str) -> list:
    """
    :rtype: Elements
    """
    session.commit() # 提交一次，防止查询缓存
    logging.info("接受到查询请求,请求参数为: " + str(deviceType))
    # 返回列表，一个设备类型有多个报警/故障
    result = session.query(Device_info).filter_by(device_type=deviceType).all()
    session.close()
    return result


# 根据平台id查询平台下的所有数据
def search_device_by_pid(pid: int) -> Config:
    """
    :rtype: Elements
    """
    logging.info("接受到查询请求,请求参数为: " + str(pid))
    resultList = session.query(Device).filter_by(p_id=pid).all()
    return resultList


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


if __name__ == '__main__':
    time1 = datetime.datetime.fromtimestamp(1669105781)
    time2 = datetime.datetime.fromtimestamp(1669105053)
    time_difference = time2 - time1
    print(time_difference.seconds)
