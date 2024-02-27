global testFlage

def listenFunc(func):
    def obtainFunce(*args, **kwargs):
        testFlage = globals().get('testFlage')
        # 将需要执行得方法返回
        try:
            func(*args, **kwargs)
        except AssertionError as e:
            testFlage = True
        if testFlage == True:
            assert 1 != 1

    return obtainFunce
