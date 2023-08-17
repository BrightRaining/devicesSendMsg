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
    time1 = datetime.datetime.fromtimestamp(1669105781)
    time2 = datetime.datetime.fromtimestamp(1669105053)
    time_difference = time2 - time1
    print(time_difference.seconds)