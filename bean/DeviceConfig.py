class DeviceConfig():
    deviceId = 1
    code = 1
    devicePrefix = 1
    deviceType = 'SMR3100'

    def __init__(self, deviceId,devicePrefix,code,deviceType):
        self.deviceId = deviceId #设备id
        self.code = code # 协议主体
        self.devicePrefix = devicePrefix # 协议前缀
        self.deviceType = deviceType # 设备类型
