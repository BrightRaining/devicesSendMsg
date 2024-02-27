# -*- coding:UTF-8 -*-
import asyncio
import datetime
import hashlib
import json
import random
import re
import time

import requests

from batchdata import ActDevAlarm


def setGlobaBatchlSession(login):
    global loginBatchSession
    loginBatchSession = login


def getGlobalBatchLogin():
    if globals() == None or globals().get('loginBatchSession') == None:
        return None
    else:
        return globals().get("loginBatchSession")


# 生成当前时间的时间戳，只有一个参数即时间戳的位数，默认为10位，输入位数即生成相应位数的时间戳，比如可以生成常用的13位时间戳
def now_to_timestamp(digits=10):
    time_stamp = time.time()
    digits = 10 ** (digits - 10)
    time_stamp = int(round(time_stamp * digits))
    return time_stamp


def loginSession(urlDomain, userName, pwd):
    url = urlDomain + "/self_operator/login"
    h = hashlib.md5()
    h.update(str(pwd).encode("utf8"))
    t = {"username": userName, "password": h.hexdigest(), "code": "tpson",
         'key': "96899b63-c59a-46c3-b4ed-aa6bbc751b05"}
    req = requests.post(url, data=t)
    session = req.cookies.get("SESSION")
    ## Authorization
    authorization = req.json()['data']['jwtToken']
    setGlobaBatchlSession({"Cookie": "SESSION=" + str(session),"Authorization":authorization})
    return {"Cookie": "SESSION=" + str(session),"Authorization":authorization}


# 批量新增单位
class BatchAddDept:

    def addBatchDept(self, urlDomain, userName, pwd, deptNum, isAssBuild, pageSize, assBandNum):
        """
        批量新增单位
        :param urlDomain: 域名
        :param userName: 登录账号
        :param pwd: 登录密码
        :param deptNum: 新增单位的数量 新增数量如果需要100个，数值要填101
        :param isAssBuild: 是否绑定建筑
        :param pageSize: 查询建筑的页数
        :param assBandNum: 一个单位绑定建筑的数量
        :return:
        """
        url = urlDomain + '/self_operator/department/v2/save'
        # 判断全局是否存在session
        loginBatchSession = getGlobalBatchLogin()

        # 判断是否需要进行登录
        if loginBatchSession is None:
            loginBatchSession = loginSession(urlDomain, userName, pwd)

        # 真代表需要组织关联楼栋则进入查询楼栋id
        if isAssBuild:
            deptSearchUrl = urlDomain + '/self_operator/building/page?departmentId=0&pageNumber=1&pageSize=' + str(
                pageSize)
            req = requests.get(deptSearchUrl, headers=loginBatchSession)
            buildList = req.json()
            # print(buildList)

        print(loginBatchSession)
        # 控制新增多少单位 这里的1不能变成0，不然下面的代码处理会很麻烦
        for i in range(1, deptNum):
            saveData = {
                "name": "自动新增" + str(time.time()),
                "geographicId": "330108002",
                "posX": "30.1780510",
                "posY": "120.1896940",
                "posZ": "16",
                "location": "234",
                "pid": 0  # 控制当前新增部门的父级单位默认是顶级，需要更换自行到组织单位模块查找查询接口的parentId进行更换
            }
            if isAssBuild:
                buildIds = ''
                # 组织单位关联楼栋数量默认50
                totalList = buildList['data']['total']
                for k in range((i - 1) * int(assBandNum), i * int(assBandNum)):
                    buildArray = buildList['data']['list']
                    if (totalList - 1) > k:
                        buildId = buildArray[k]['id']
                        if buildIds == '':
                            buildIds = buildIds + str(buildId)
                        else:
                            if buildIds.find(str(buildId)) < 0:
                                buildIds = buildIds + ',' + str(buildId)
                    else:
                        buildId = buildArray[random.randint(0, (totalList - 1))]['id']
                        if buildId != '' and buildId is not None and buildIds.find(str(buildId)) < 0:
                            buildIds = buildIds + ',' + str(buildId)
                print(buildIds)
                saveData['buildingIds'] = buildIds
            req = requests.post(url, data=saveData, headers=loginBatchSession, )
            print("请求接口：" + req.url)
            print("请求参数：" + req.request.body)
            print(req.text)


class BatchAddBuild:

    def batchAddBuid(self, urlDomain, userName, pwd, addBuildNum):

        """
        批量新增楼栋
        :param urlDomain: 域名
        :param userName: 登录名
        :param pwd: 密码
        :param addBuildNum: 添加建筑的数量
        :return:
        """

        url = urlDomain + '/self_operator/building/v2/save'
        # 判断全局是否存在session
        loginBatchSession = getGlobalBatchLogin()
        # 判断是否需要进行登录
        if loginBatchSession is None:
            loginBatchSession = loginSession(urlDomain, userName, pwd)
        conact = urlDomain + '/self_operator/user/contact/add'
        # 需要先新增联系人
        addUserData = {
            "name": "自动新增用户",
            "phone": "13329229689",
            "departmentId": 0
        }
        req = requests.post(conact, data=addUserData, headers=loginBatchSession)
        conactId = None
        if req.text.find("存在") > 0:
            conactList = urlDomain + '/self_operator/user/contact/page?pageNumber=1&pageSize=10&name=&phone=&departmentId='
            req = requests.get(conactList, headers=loginBatchSession)
            conactId = req.json()['data']['list'][0]['id']
        else:
            conactId = req.json()['data']
        print(req.text)

        # 下面是新增楼栋

        for i in range(0, addBuildNum):
            saveData = {
                "name": "自动新增楼栋" + str(time.time()),
                "groundCount": 5,  # 楼层数 默认5层
                "undergroundCount": 5,  # 地下楼层数，默认5层
                "departmentIds": 0,  # 绑定部门ids，新增时默认顶级部门即可
                "fireResponsibleContact[0].name": "",
                "fireResponsibleContact[0].phone": "",
                "fireResponsibleContact[0].id": str(conactId),
                "posX": "120.192752",
                "posY": "30.347952",
                "geographicId": "330108002",
                "position": "临丁路上塘河衣锦桥下古纤道",
                "departmentId": 0  # 绑定部门不用管默认即可
            }

            req = requests.post(url, data=saveData, headers=loginBatchSession, )
            print("请求接口：" + req.url)
            print("请求参数：" + req.request.body)
            print(req.text)


class BatchAddDevices:

    def batchSendDevAlarmAndFault(self, host, port, initDeviceCode, deviceNum):
        # 切割初始设备id进行自增长
        devPre = ''.join(re.findall(r'[A-Za-z]', initDeviceCode))
        devEndP = initDeviceCode.split(devPre)  # 英文部分
        devEnd = int(devEndP[1])  # 数字部分
        tasks = []
        for i in range(0, deviceNum):
            # ActDevAlarm.sendSelfDeviceFault(host, port, str(devPre + str(int(devEnd) + int(i))))  # 故障
            # ActDevAlarm.sendSelfDeviceAlarm(host, port, str(devPre + str(int(devEnd) + int(i))))  # 报警 此处产生1w条报警
            # tasks = [ActDevAlarm.sendSelfDeviceAlarm(host, port, str(devPre + str(int(devEnd) + int(i))))]
            tasks.append(asyncio.ensure_future(ActDevAlarm.sendSelfDeviceAlarm(host, port, str(devPre + str(int(devEnd) + int(i))))))
            tasks.append(asyncio.ensure_future(ActDevAlarm.sendSelfDeviceFault(host, port, str(devPre + str(int(devEnd) + int(i))))))

            print(str(devPre + str(int(devEnd) + int(i))))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

    def batchSendDevData(self, host, port, initDeviceCode, deviceNum):
        """
        发送对应设备的实时数据
        :param host:
        :param port:
        :param initDeviceCode:
        :param deviceNum:
        :return:
        """
        # 切割初始设备id进行自增长
        devPre = ''.join(re.findall(r'[A-Za-z]', initDeviceCode))
        devEndP = initDeviceCode.split(devPre)  # 英文部分
        devEnd = int(devEndP[1])  # 数字部分
        for i in range(0, deviceNum):
            # 实时数据
            ActDevAlarm.sendDeviceRealData(host,port,str(devPre + str(int(devEnd) + int(i))),i)
            print(str(devPre + str(int(devEnd) + int(i))))
            time.sleep(2)



    def batchAddDev(self, urlDomain, userName, pwd, initDeviceCode, deviceNum, devicesModelName, modelType=3,host='0.0.0.0',port='7893'):

        """
            批量添加设备
        :param urlDomain: 域名
        :param userName: 登录账号
        :param pwd: 登录密码
        :param initDeviceCode: 初始设备编号,必须是英文在前数字在后
        :param deviceNum: 添加设备的数量
        :param devicesModelName: 设备型号
        :param modelType: 物联设备的类型：是用电/烟感/用水 1-烟感，3-用电，6-用水，21-微型断路器
        :return:
        """

        url = urlDomain + '/self_operator/device/save'
        # 判断全局是否存在session
        loginBatchSession = getGlobalBatchLogin()
        # 判断是否需要进行登录
        if loginBatchSession is None:
            loginBatchSession = loginSession(urlDomain, userName, pwd)

        # 获取对应类型设备的设备型号和系统类型
        modelUrl = urlDomain + '/self_operator/device/model/list?deviceType=' + str(modelType)
        req = requests.get(modelUrl, headers=loginBatchSession)
        dataModel = req.json()['data']
        tarModel = None
        systemType = None
        for model in dataModel:
            modelName = model['name']
            if modelName == devicesModelName:
                tarModel = model['id']

        systemUrl = urlDomain + '/self_operator/device/system_type_v2/list?deviceType=' + str(modelType)
        req = requests.get(systemUrl, headers=loginBatchSession)
        systemType = req.json()['data'][0]['id']  # 默认取第一个

        # 如果没找到对应的设备型号，终止此次添加
        if tarModel is None:
            print('未找到适合设备的型号')
            return ''

        # 获取楼栋列表 默认前100个
        deptSearchUrl = urlDomain + '/self_operator/building/page?departmentId=0&pageNumber=1&pageSize=1000'
        req = requests.get(deptSearchUrl, headers=loginBatchSession)
        buildList = req.json()
        buildArray = buildList['data']['list']

        # 切割初始设备id进行自增长
        devPre = ''.join(re.findall(r'[A-Za-z]', initDeviceCode))
        devEndP = initDeviceCode.split(devPre)  # 英文部分
        devEnd = devEndP[1]  # 数字部分

        # 新增设备时的预备数据，只支持室内
        saveData = {
            'code': '',  # 设备编码
            'departmentId': 150,  # 绑定的部门id
            'model': tarModel,  # 设备类型id,例如：3002对应的id是0，不要随意变动，参考参数备注传值即可
            'communicationMode': 1,  # 通讯方式默认4G通用
            'name': '',  # 设备名称 和 设备编码保持一致
            'type': modelType,  # 设备类型，烟感/用电这种大类
            'systemTypeV2': systemType,  # 系统类型
            'buildingId': 352,
            'floorId': 493,
            'geographicId': '',
            'isOutdoor': False,
            'posX': '0.41796875',
            'posY': '0.35003662109375',
            'position': '杭州市博文小学',
            'automaticLinkage': False,
        }

        for i in range(0, deviceNum):
            totalList = buildList['data']['total']
            # 每次都会随机在楼栋集合ID中取出一个
            randomNum = random.randint(0, (totalList - 1))
            buildData = buildArray[randomNum]
            buildId = buildData['id']
            departmentIds = buildData['departmentIds']
            departmentLen = tuple(departmentIds).__len__()

            floorCount = buildData['floorCount']
            if floorCount <= 0:
                print('存在楼栋中没有楼层无法进行')
                return
            # 查找楼层
            floorUrl = urlDomain + '/self_operator/floor/v2/list?buildingId=' + str(buildId)
            floorReq = requests.get(floorUrl, headers=loginBatchSession)
            floorListData = floorReq.json()['data']
            floorId = floorListData[random.randint(0, (floorCount - 1))]['id']
            saveData['code'] = str(devPre + str(int(devEnd) + int(i)))
            saveData['name'] = str(devPre + str(int(devEnd) + int(i)))
            saveData['buildingId'] = buildId
            saveData['floorId'] = floorId
            saveData['departmentId'] = departmentIds[random.randint(0, int(departmentLen) - 1)]
            req = requests.post(url, data=saveData, headers=loginBatchSession)

            # if req.ok:
            #     # ActDevAlarm.sendDeviceRealData(str(host), str(port), str(devPre + str(int(devEnd) + int(i))),0)
            #     ActDevAlarm.sendSelfDeviceAlarm(str(host), str(port), str(devPre + str(int(devEnd) + int(i))))  # 报警数据触发
            #     ActDevAlarm.sendSelfDeviceFault(host, port, str(devPre + str(int(devEnd) + int(i)))) # 故障数据触发

            print("请求接口：" + req.url)
            # time.sleep(1)
            # timer = time.strftime("%Y-%m-%d %H:%M:%S")
            # print("请求参数：" + str(timer) + req.request.body)
            print(req.text)


if __name__ == '__main__':
    # 请求域名后不要带 /
    url = 'http://192.168.0.188:8884'
    userName = 'tpson003'
    pwd = 'Tpson123456'
    # 批量新增楼栋，此处不设置组织单位绑定
    # BatchAddBuild().batchAddBuid(url, userName, pwd, 20)
    # #
    # # 批量新增组织单位和绑定建筑，如果是全新企业需要新增建筑才能设置True，新增数量如果需要100个，数值要填101
    # BatchAddDept().addBatchDept(url, userName, pwd, 10, True, 1001, 20)

    # 批量新增设备 modelType[方法的最后一个参数]: 物联设备的类型： 1-烟感，3-用电，6-用水，21-微型断路器
    BatchAddDevices().batchAddDev(url, userName, pwd, 'DJ20040088', 200, "SMR1210", 6,host='192.168.0.188',port='7893')

    # 对已有设备发送报警/故障设备
    # BatchAddDevices().batchSendDevAlarmAndFault('192.168.0.214', '7893', 'IA21090097', 23)
    # BatchAddDevices().batchSendDevData('192.168.0.214', '7893', 'AM20190078', 1)
    # time.sleep(100000)
