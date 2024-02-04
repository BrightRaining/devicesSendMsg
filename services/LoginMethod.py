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
        if globals().get("loginSession") is None:
            if config.status != 1 :
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
            # session = globals().get("loginSession")
    except Exception as e:
        print(e)
if __name__ == '__main__':
    s = '478984698wrwerwewe23423'
    p = '46'
    print(s.find(p))