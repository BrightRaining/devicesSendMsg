import re

import requests
from flask import request
from flask import Flask

from bean.ConfigData import ConfigData
from services.DeviceAlarmService import DeviceAlarmService

flask = Flask(__name__)
flask.config["JSON_AS_ASCII"] = False


@flask.route("/device", methods=['GET'])
def deviceTrgger():
    # 发送来的请求体
    # 提取项目id
    trigger = request.args.get('trigger', default=1)  # 触发次数
    triggerType = request.args.get('triggerType', default=1)  # 触发类型
    randomTrigger = request.args.get('randomTrigger', default=1)  # 触发次数

    host = request.args.get('host', default='192.168.0.214')  # 触发次数
    port = request.args.get('port', default='7893')  # 触发次数
    deviceId = request.args.get('deviceId', default='005H20232023003')  # 设备id
    deviceType = request.args.get('deviceType', default='RTU500')  # 设备类型

    print(host + ":" + port)

    configData = ConfigData()
    configData.trigger = trigger
    configData.triggerType = triggerType
    configData.randomTrigger = randomTrigger

    DeviceAlarmService().deviceAlarm(host,port,deviceId,deviceType,configData)
    return {"code": "SUCCESS"}


flask.run(host='10.0.0.32')
