import numpy as np
from locust import HttpUser, TaskSet, task, between

INPUT_WIDTH = 10


class PredictTaskSetUser(HttpUser):
    '''
    @task(1)
    def predict(self):
        payload = {
            'input': np.random.random((1, INPUT_WIDTH)).tolist()
        }
        self.client.post('/predict', json=payload)
    '''

    def on_start(self):
        payload = {
            'input': np.random.random((1, INPUT_WIDTH)).tolist()
        }
        self.client.post('/predict', json=payload)

'''
class PredictLocust(HttpUser):
    task_set = PredictTaskSet
    wait_time = between(1, 3)
'''

	
