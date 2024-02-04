# CRC-16-MODBUS
import random
import re
import time

from bean.ConfigData import ConfigData
from bean.DeviceConfig import DeviceConfig
from db import DbData
from devicedb import ImDeviceDbData
from tcpConnUtils import TcpUtils


def calculate_crc16(data: bytes) -> int:
    # 初始化crc为0xFFFF
    crc = 0xFFFF

    # 循环处理每个数据字节
    for byte in data:
        # 将每个数据字节与crc进行异或操作
        crc ^= byte

        # 对crc的每一位进行处理
        for _ in range(8):
            # 如果最低位为1，则右移一位并执行异或0xA001操作(即0x8005按位颠倒后的结果)
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            # 如果最低位为0，则仅将crc右移一位
            else:
                crc = crc >> 1

    # 返回最终的crc值
    return crc


# def device_code_config(host, port, deviceId, code,deviceConfig:DeviceConfig): 4040 +流水号+id+xxxxxxxxx +校验码(4位) +2323
def device_code_config(host, port, deviceConfig: DeviceConfig):
    # 10 进制转16进制
    hex_str = deviceConfig.deviceId.encode('utf-8').hex().upper()
    devEndCode = str(deviceConfig.code)
    # 将截尾的时间戳剔除
    restCode = devEndCode[0: devEndCode.__len__() - 8]
    timestamp = int(time.time())
    rest = str(hex(timestamp).upper())
    # 换成当前时间，不包含设备ID前得数据
    result1 = str(restCode) + rest[2:]
    tesc = None
    # 替换流水号的方法 和3100类型流水号在 6位得可以直接在这里加上
    if deviceConfig.deviceType == 'MCB2000':
        print(str(str(deviceConfig.devicePrefix) + (hex_str) + result1))
        scpN = str(deviceConfig.devicePrefix) + (hex_str)
        tesc = replaceDeviceSerialNumberSimilarMCB2000(scpN.__len__(),str(deviceConfig.devicePrefix) + (hex_str) + result1)
    # 替换流水号的方法 和3100类型流水号在前6位得可以直接在这里加上
    elif deviceConfig.deviceType == 'SMR3100' or deviceConfig.deviceType == 'EMR3002' :
        tesc = replaceDeviceSerialNumberSimilarSMR3100(str(deviceConfig.devicePrefix) + (hex_str) + result1)
    # 替换流水号的方法 和1003类型相似得流水号在消息体中的设备类型直接在这里加上
    elif deviceConfig.deviceType == 'EMR1003' or deviceConfig.deviceType == 'RTU500' or deviceConfig.deviceType == 'EMR1002':
        result = replaceDeviceSerialNumberSimilarEMR1003(result1)
        tesc = str(deviceConfig.devicePrefix) + (hex_str) + result
    elif deviceConfig.deviceType == 'SMR1210':
        s = '02'
        num = random.randint(5000, 9999)
        cp = str(hex(num))
        tesc = s + cp[2:] + hex_str + result1
    else:
        tesc = str(deviceConfig.devicePrefix) + (hex_str) + result1
    # 测试数据 -crc校验 6BE1
    test_data = bytes.fromhex(tesc)
    # 计算CRC-16校验码
    crc16 = calculate_crc16(test_data)
    codeDid = '4040' + tesc + str(f'{crc16:04X}') + '2323'
    # time.sleep(1)  # 暂停2s
    print('发送的协议：' + str(codeDid))
    TcpUtils.tcp_con(host, port, codeDid)


# 替换流水号的方法 和1003类型相似得流水号在消息体中的设备类型直接引用
def replaceDeviceSerialNumberSimilarMCB2000(stNum,repCode):
    # 替换随机四位流水号准备
    num = random.randint(4000, 9999)
    cp = str(hex(num))
    # 取出前4位
    # 再取前4位，成功剥离流水号
    result = repCode[0:int(stNum+10)] + cp[2:] + repCode[int(stNum+14):repCode.__len__()]
    return result


# 替换流水号的方法 和1003类型相似得流水号在消息体中的设备类型直接引用
def replaceDeviceSerialNumberSimilarEMR1003(repCode):
    # 替换随机四位流水号准备
    num = random.randint(4000, 9999)
    cp = str(hex(num))
    # 取出前4位
    # 再取前4位，成功剥离流水号
    result = repCode[0:8] + cp[2:] + repCode[12:repCode.__len__()]
    return result


# 替换流水号的方法 和3100类型流水号在前6位得可以直接使用，流水号开头必须大于4
def replaceDeviceSerialNumberSimilarSMR3100(repCode):
    # 替换随机四位流水号准备
    num = random.randint(4000, 9999)
    cp = str(hex(num))
    # 取出前4位
    # 再取前4位，成功剥离流水号
    result = repCode[0:2] + cp[2:] + repCode[6:repCode.__len__()]
    print(result)
    return result


class DeviceAlarmService:

    def deviceAlarm(self, host, port, deviceId, deviceType, configData: ConfigData):
        """
            新增设备时发送该消息进行激活
            :param host: 通讯地址
            :param port: 通讯端口
            :param deviceId: 设备编号
            :param deviceType: 设备类型
            :param configData: 如何触发报警的配置类
            :return:
        """
        deviceList = DbData.search_tab_by_type_devices(deviceType)
        if deviceList.__len__() <= 0:
            return {"msg": "未查到输入的设备型号", "tips": "目前支持的设备型号：EMR3002,RTU500,SMR3100,EMR1002,SMR3250的部分报警和故障", }
        # 触发报警
        trggerNum = configData.trigger
        # 如果传入的随机数大于该类型设备的报警数则以报警数为准
        if deviceList.__len__() - configData.trigger < 0:
            trggerNum = deviceList.__len__() - 1
        # 触发报警的次数
        for i in range(0, trggerNum):
            # 如果是随机触发，则使用随机数
            if configData.randomTrigger == 1:
                randomNum = random.randint(0, (deviceList.__len__() - 1))
                # 报警和故障都要触发
                if configData.triggerType == 3:
                    if deviceList[randomNum].device_alarm is not None and str(deviceList[randomNum].device_alarm) != '':
                        deviceConfig = DeviceConfig(deviceId, deviceList[randomNum].device_prefix,
                                                    deviceList[randomNum].device_alarm,
                                                    deviceList[randomNum].device_type)
                        device_code_config(host, port, deviceConfig)
                    # print(deviceList[randomNum].device_alarm)
                    if deviceList[randomNum].device_fault is not None and str(deviceList[randomNum].device_fault) != '':
                        deviceConfig = DeviceConfig(deviceId, deviceList[randomNum].device_prefix,
                                                    deviceList[randomNum].device_fault,
                                                    deviceList[randomNum].device_type)
                        device_code_config(host, port, deviceConfig)
                    # print(deviceList[randomNum].device_fault)
                # 报警
                if configData.triggerType == 1:
                    if deviceList[randomNum].device_alarm is not None and str(deviceList[randomNum].device_alarm) != '':
                        deviceConfig = DeviceConfig(deviceId, deviceList[randomNum].device_prefix,
                                                    deviceList[randomNum].device_alarm,
                                                    deviceList[randomNum].device_type)
                        device_code_config(host, port, deviceConfig)
                        # print(deviceList[randomNum].device_alarm)
                # 故障
                if configData.triggerType == 2:
                    if deviceList[randomNum].device_fault is not None and str(deviceList[randomNum].device_fault) != '':
                        deviceConfig = DeviceConfig(deviceId, deviceList[randomNum].device_prefix,
                                                    deviceList[randomNum].device_fault,
                                                    deviceList[randomNum].device_type)
                        device_code_config(host, port, deviceConfig)

                # 报警触发的同时还需恢复
                if configData.triggerType == 4:
                    deviceConfig = DeviceConfig(deviceId, deviceList[randomNum].device_prefix,
                                                deviceList[randomNum].device_alarm, deviceList[randomNum].device_type)
                    device_code_config(host, port, deviceConfig)
                    deviceConfig.code = deviceList[randomNum].device_device_alarm_restore
                    device_code_config(host, port, deviceConfig, )
                    # print(deviceList[randomNum].device_device_alarm_restore)

                # 故障触发的同时还需恢复
                if configData.triggerType == 5:
                    device_code_config(host, port, deviceId)
                    deviceConfig = DeviceConfig(deviceId, deviceList[randomNum].device_prefix,
                                                deviceList[randomNum].device_fault, deviceList[randomNum].device_type)
                    device_code_config(host, port, deviceConfig)
                    deviceConfig.code = deviceList[randomNum].device_device_fault_restore
                    device_code_config(host, port, deviceConfig, )
                    # print(deviceList[randomNum].device_device_fault_restore)
            else:
                # 不是随机触发，则按顺序触发即可
                if configData.triggerType == 1:
                    if deviceList[i].device_alarm is not None and str(
                            deviceList[i].device_alarm) != '':
                        deviceConfig = DeviceConfig(deviceId, deviceList[i].device_prefix,
                                                    deviceList[i].device_alarm, deviceList[i].device_type)
                        device_code_config(host, port, deviceConfig)

                if configData.triggerType == 2:
                    if deviceList[i].device_fault is not None and str(
                            deviceList[i].device_fault) != '':
                        deviceConfig = DeviceConfig(deviceId, deviceList[i].device_prefix,
                                                    deviceList[i].device_fault, deviceList[i].device_type)
                        device_code_config(host, port, deviceConfig)

                if configData.triggerType == 3:
                    deviceConfig = DeviceConfig(deviceId, deviceList[i].device_prefix,
                                                deviceList[i].device_alarm, deviceList[i].device_type)
                    device_code_config(host, port, deviceConfig)
                    if deviceList[i].device_fault is not None and str(
                            deviceList[i].device_fault) != '':
                        deviceConfig = DeviceConfig(deviceId, deviceList[i].device_prefix,
                                                    deviceList[i].device_fault, deviceList[i].device_type)
                        device_code_config(host, port, deviceConfig)

        return {"code": "SUCCESS", "tips": "发送成功,若无弹窗请检查参数和平台环境"}


if __name__ == '__main__':
    configData = ConfigData()
    configData.trigger = 1
    configData.randomTrigger = 2
    configData.triggerType = 1
    # configData.triggerType = 3 # 都触发

    # http://192.168.0.251:5000/device?host=192.168.0.214&port=7893&deviceId=SM20230303&deviceType=EMR1002
    msg = DeviceAlarmService().deviceAlarm('47.110.73.94', '17893', 'DJ20230005', 'SMR1210', configData)
    print(msg)

    # # 切割初始设备id进行自增长
    # initDeviceCode = 'EMR20233101'
    # devPre = ''.join(re.findall(r'[A-Za-z]',initDeviceCode))
    # devEndP = initDeviceCode.split(devPre)  # 英文部分
    # devEnd = int(devEndP[1])  # 数字部分
    # i = 1
    # while True:
    #     # http://192.168.0.251:5000/device?host=192.168.0.214&port=7893&deviceId=SM20230303&deviceType=EMR1002
    #     print("开始:" + str(devPre + str(int(devEnd) + int(i))))
    #     msg = DeviceAlarmService().deviceAlarm('10.0.0.193', '7893', str(devPre + str(int(devEnd) + int(i))), 'EMR1003',
    #                                            configData)
    #     i = i+1
    #     if i >= 496:
    #         i = 1
    #     print(str(msg) + ":" + str(devPre + str(int(devEnd) + int(i))))

    # for i in range(1, 2500):
    #     # http://192.168.0.251:5000/device?host=192.168.0.214&port=7893&deviceId=SM20230303&deviceType=EMR1002
    #     print("开始:" + str(devPre + str(int(devEnd) + int(i))))
    #     msg = DeviceAlarmService().deviceAlarm('10.0.0.193', '7893', str(devPre + str(int(devEnd) + int(i))), 'EMR1003', configData)
    #     print(str(msg) + ":"+ str(devPre + str(int(devEnd) + int(i))))
