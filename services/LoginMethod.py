# -*- coding:UTF-8 -*-

import hashlib
import requests

from bean import interface_address
from db import DbData
from db.Elements import Config


def setGlobalSession(login):
    global loginSession
    loginSession = login


def getGlobalLogin():
    if globals() == None or globals().get('loginSession') == None:
        return None
    else:
        return globals().get("loginSession")


def login_user(config:Config):
    try:
            h = hashlib.md5()
            # 密码转换
            h.update(str(config.pwd).encode("utf8"))
            t = {"username": config.userName, "password": h.hexdigest(), 'code': 'tpson','key':'2c9f00b4-f845-4769-9d0c-43aa54134c9e'}
            req = requests.post(config.platformPrefix+interface_address.login_address, data=t)
            reqJson = req.json()
            jwtToken = reqJson['data']['jwtToken']
            token = reqJson['data']['token']
            session = {'Authorization':jwtToken,'Cookie':'SESSION='+str(token)}
            setGlobalSession(session)
    except Exception as e:
        print(e)
if __name__ == '__main__':
    import time
    timestamp = time.time()  # 获取当前时间戳
    formatted_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(timestamp))  # 将时间戳转换为格式化字符串
    print(formatted_time)  # 输出格式化后的日期时间字符串