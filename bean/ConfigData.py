class ConfigData:
    trigger = 1  # 触发几次
    triggerType = 1  # 触发类型 1报警，2故障，3故障和报警都要触发，4：触发报警的同时还要恢复，5：触发故障的同时还要恢复
    randomTrigger = 1  # 1：随机触发该类设备的任意报警/故障 xx次，2：顺序触发报警/故障

    def __int__(self, trigger, triggerType, randomTrigger):
        self.trigger = trigger  # 触发几次
        self.triggerType = triggerType  # 触发类型 1报警，2故障，3故障和报警都要触发，4：触发报警的同时还要恢复，5：触发故障的同时还要恢复
        self.randomTrigger = randomTrigger  # 1：随机触发该类设备的任意报警/故障 xx次，2：顺序触发报警/故障
