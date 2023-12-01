class DeviceConfig():
    deviceId = 1
    code = 1
    devicePrefix = 1
    deviceType = 'SMR3100'

    def __init__(self, deviceId,devicePrefix,code,deviceType):
        self.deviceId = deviceId
        self.code = code
        self.devicePrefix = devicePrefix
        self.deviceType = deviceType
