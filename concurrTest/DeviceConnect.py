from locust import task,TaskSet,HttpUser


class DeviceConnect(TaskSet):

    @task
    def taskAlarmList(self):
        self.client.get()