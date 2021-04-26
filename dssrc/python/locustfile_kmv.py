from locust import HttpUser, task, between
import json
import os

json_data =""
g_scnt = 0
g_kcnt = 0

class PredictTaskUser(HttpUser):
    wait_time = between(0.5,1)

    @task(1)
    def kmv(self):
        global g_kcnt
        l_kcnt=0
        if g_kcnt % 50 == 0:
            print("pid, g_kcnt, l_kcnt :", os.getpid(), g_kcnt, l_kcnt)
        # print("on_kmv :", type(json_data))
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.client.post('/kmv', data=json.dumps(json_data), headers=headers)
        g_kcnt += 1
        l_kcnt += 1

    def on_start(self):
        global json_data, g_scnt
        l_scnt=0
        with open("/application/mds/dssrc/data/client/java_kmv_input.json", "r") as fp:
            json_data = json.load(fp)

        # print("on_start :", type(json_data))
        print("pid, g_scnt, l_scnt :", os.getpid(), g_scnt, l_scnt)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.client.post('/kmv', data=json.dumps(json_data), headers=headers)
        g_scnt += 1
        l_scnt += 1


	

