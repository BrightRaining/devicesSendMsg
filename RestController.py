import re

import requests
from flask import request
from flask import Flask

from bean.ConfigData import ConfigData
from services.DeviceAlarmService import DeviceAlarmService

flask = Flask(__name__)
flask.config["JSON_AS_ASCII"] = False

# flask.json.ensure_ascii = False # Linux 解决中文乱码

# 示范链接：http://10.0.0.32:5000/device?host=192.168.0.214&deviceId=005H20232023003&deviceType=RTU500
# 正式环境示范连接：http://10.0.0.32:5000/device?host=14.18.73.163&deviceId=AM21050022&deviceType=EMR3002
# 数字电力测试环境：http://192.168.0.251:5000/device?host=47.110.73.94&port=18893&deviceId=EMR2023114&deviceType=EMR3002

# Linux环境指定下载源：pip3 install requests  -i https://pypi.tuna.tsinghua.edu.cn/simple
# 下载源地址：https://blog.csdn.net/weixin_46713695/article/details/125080772
# 安装SQLAlchemy==1.4.36 之前需要先安装 greenlet==1.1.2
# 将程序挂载到后台,并记录执行日志： nohup python3 RestController.py >> /home/pythonWork/ims.log 2>1&
# 查找进程：ps -def |grep RestController.py
# http://192.168.0.251:5000/device?host=192.168.0.214&port=7893&deviceId=IA21090097&deviceType=SMR3100
@flask.route("/device", methods=['GET'])
def deviceTrgger():
    # 发送来的请求体
    # 提取项目id
    trigger = request.args.get('trigger', default=1)  # 触发次数
    triggerType = request.args.get('triggerType', default=1)  # 触发类型
    randomTrigger = request.args.get('randomTrigger', default=1)  # 触发次数
    host = request.args.get('host', default='47.110.73.94')  # 触发次数
    port = request.args.get('port', default='17893')  # 触发次数
    deviceId = request.args.get('deviceId', default='AA12345678')  # 设备id
    deviceType = request.args.get('deviceType', default='EMR3002')  # 设备类型
    print(host + ":" + port)
    configData = ConfigData()
    configData.trigger = trigger
    configData.triggerType = triggerType
    configData.randomTrigger = randomTrigger
    msg = DeviceAlarmService().deviceAlarm(host,port,deviceId,deviceType,configData)
    return msg


flask.run(host='10.0.0.32', threaded=True)
# flask.run(host='192.168.0.251')
