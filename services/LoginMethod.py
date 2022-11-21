#-*- coding:UTF-8 -*-

import hashlib
import requests

from db.DbData import search_tab_config

def setGlobalSession(login):
    global loginSession
    loginSession = login


def getGlobalLogin():
    if globals() == None or globals().get('loginSession') == None:
        return None
    else:
        return globals().get("loginSession")

def login_user():
    try:
        ele_list = search_tab_config()
        if globals().get("loginSession") is None:
            loginSession = {}
            for k in ele_list:
                if k.status == "1":
                    if k.platformType in '2':
                        url = k.platformPrefix + ':' + k.platformPort
                        h = hashlib.md5()
                        h.update(str(k.pwd).encode("utf8"))
                        t = {"username": k.userName, "password": h.hexdigest()}
                        req = requests.post(url, json=t)
                        session = req.cookies.get("SESSION")
                        loginSession[k.id] = session
                    else:
                        url = k.platformPrefix + ':' + k.platformPort
                        h = hashlib.md5()
                        h.update(str(k.pwd).encode("utf8"))
                        t = {"username": k.userName, "password": h.hexdigest()}
                        req = requests.post(url, data=t)
                        session = req.cookies.get("SESSION")
                        loginSession[k.id] = session
                setGlobalSession(loginSession)
        session = globals().get("loginSession")
        print(session)
    except Exception as e:
        print(e)
