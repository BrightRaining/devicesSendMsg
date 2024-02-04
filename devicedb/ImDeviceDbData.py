#-*- coding:UTF-8 -*-

import datetime
import hashlib
import logging
import re
import time
from sqlalchemy.orm import sessionmaker

from devicedb.ImElements import Device_info, Device
from devicedb.Imbase import engine

Session = sessionmaker(bind=engine)
session = Session()

def search_devices_info() -> list:
    """
    :rtype: object
    """
    # 165
    ele_list = session.query(Device_info).all()
    session.close()
    return ele_list


# 根据设备类型查询数据
def search_tab_by_id_devices(deviceType: str) -> list:
    """
    :rtype: Elements
    """
    session.commit() # 提交一次，防止查询缓存
    logging.info("接受到查询请求,请求参数为: " + str(deviceType))
    # 返回列表，一个设备类型有多个报警/故障
    result = session.query(Device_info).filter_by(device_type=deviceType).all()
    session.close()
    return result

# 根据设备id查询设备信息
def search_device_by_did(device_code1: str):
    result = session.query(Device).filter_by(device_code=device_code1).all()
    return result


# 查Device询整张表的数据
def search_device() -> list:
    # 返回所有的设备列表
    result = session.query(Device).all()
    return result


def search_device_all(deviceType: str):
    session.commit()  # 提交一次，防止查询缓存
    logging.info("接受到查询请求,请求参数为: " + str(deviceType))
    # 返回列表，一个设备类型有多个报警/故障
    result = session.query(Device_info, Device).join(Device, Device_info.device_type == Device.device_type).all()
    for device in result:
        print(device.id)





if __name__ == '__main__':
    deviceList = search_tab_by_id_devices('EMR1003')
    for i in range(0,deviceList.__len__()-1):
        print(deviceList[i].device_alarm)
