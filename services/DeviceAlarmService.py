# CRC-16-MODBUS
import logging
import random

from bean.ConfigData import ConfigData
from bean.DeviceConfig import DeviceConfig
from devicedb import DeviceDbData
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


# def device_code_config(host, port, deviceId, code,deviceConfig:DeviceConfig):
def device_code_config(host, port, deviceConfig: DeviceConfig):
    hex_str = deviceConfig.deviceId.encode('utf-8').hex().upper()
    tesc = str(deviceConfig.devicePrefix) + (hex_str) + str(deviceConfig.code)
    # 测试数据 -crc校验 6BE1
    test_data = bytes.fromhex(tesc)
    # 计算CRC-16校验码
    crc16 = calculate_crc16(test_data)
    codeDid = '4040' + tesc + str(f'{crc16:04X}') + '2323'
    # time.sleep(1)  # 暂停2s
    print(codeDid)
    TcpUtils.tcp_con(host, port, codeDid)


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
        deviceList = DeviceDbData.search_tab_by_id_devices(deviceType)
        if deviceList.__len__() <= 0 :
            return {"msg": "未查到输入的设备型号","tips":"目前支持的设备型号：EMR3002,RTU500,SMR3100,EMR1002,SMR3250的部分报警和故障",}
        # 触发报警
        trggerNum = configData.trigger
        # 如果传入的随机数大于该类型设备的报警数则以报警数为准
        if deviceList.__len__() - configData.trigger < 0:
            trggerNum = deviceList.__len__()
        # 触发报警的次数
        for i in range(0, trggerNum):
            # 如果是随机触发，则使用随机数
            if configData.randomTrigger == 1:
                randomNum = random.randint(0, (trggerNum - 1))
                # 报警和故障都要触发
                if configData.triggerType == 3:
                    deviceConfig = DeviceConfig(deviceId, deviceList[randomNum].device_prefix,
                                                deviceList[randomNum].device_alarm)
                    device_code_config(host, port, deviceConfig)
                    logging.info(deviceList[randomNum].device_alarm)
                    # print(deviceList[randomNum].device_alarm)
                    deviceConfig = DeviceConfig(deviceId, deviceList[randomNum].device_prefix,
                                                deviceList[randomNum].device_fault)
                    device_code_config(host, port, deviceConfig)
                    # print(deviceList[randomNum].device_fault)
                    logging.info(deviceList[randomNum].device_fault)
                # 报警
                if configData.triggerType == 1:
                    deviceConfig = DeviceConfig(deviceId, deviceList[randomNum].device_prefix,
                                                deviceList[randomNum].device_alarm)
                    device_code_config(host, port, deviceConfig)
                    logging.info(deviceList[randomNum].device_alarm)
                    # print(deviceList[randomNum].device_alarm)
                # 故障
                if configData.triggerType == 2:
                    deviceConfig = DeviceConfig(deviceId, deviceList[randomNum].device_prefix,
                                                deviceList[randomNum].device_fault)
                    device_code_config(host, port, deviceConfig)
                    logging.info(deviceList[randomNum].device_fault)

                # 报警触发的同时还需恢复
                if configData.triggerType == 4:
                    deviceConfig = DeviceConfig(deviceId, deviceList[randomNum].device_prefix,
                                                deviceList[randomNum].device_alarm)
                    device_code_config(host, port, deviceConfig)
                    logging.info(deviceList[randomNum].device_alarm)
                    deviceConfig.code = deviceList[randomNum].device_device_alarm_restore
                    device_code_config(host, port, deviceConfig, )
                    logging.info(deviceList[randomNum].device_device_alarm_restore)
                    # print(deviceList[randomNum].device_device_alarm_restore)

                # 故障触发的同时还需恢复
                if configData.triggerType == 5:
                    device_code_config(host, port, deviceId)
                    deviceConfig = DeviceConfig(deviceId, deviceList[randomNum].device_prefix,deviceList[randomNum].device_fault)
                    device_code_config(host, port, deviceConfig)
                    logging.info(deviceList[randomNum].device_fault)
                    deviceConfig.code = deviceList[randomNum].device_device_fault_restore
                    device_code_config(host, port, deviceConfig, )
                    logging.info(deviceList[randomNum].device_fault)
                    # print(deviceList[randomNum].device_device_fault_restore)
            else:
                # 不是随机触发，则按顺序触发即可
                if configData.triggerType == 1:
                    deviceConfig = DeviceConfig(deviceId, deviceList[i].device_prefix,
                                                deviceList[i].device_alarm)
                    device_code_config(host, port, deviceConfig)

                if configData.triggerType == 2:
                    deviceConfig = DeviceConfig(deviceId, deviceList[i].device_prefix,
                                                deviceList[i].device_fault)
                    device_code_config(host, port, deviceConfig)
        return {"code": "SUCCESS","tips":"发送成功,若无弹窗请检查参数和平台环境"}


if __name__ == '__main__':
    configData = ConfigData()
    configData.trigger = 1
    configData.randomTrigger = 1
    # http://192.168.0.251:5000/device?host=192.168.0.214&port=7893&deviceId=SM20230303&deviceType=EMR1002
    msg = DeviceAlarmService().deviceAlarm('192.168.0.214', '7893', 'SM20230303', 'EMR1002', configData)
    print(msg)
