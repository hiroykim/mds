import numpy as np
from locust import HttpLocust, TaskSet, task, between

INPUT_WIDTH = 10


class PredictTaskSet(TaskSet):
    @task(1)
    def predict(self):
        payload = {
            'input': np.random.random((1, INPUT_WIDTH)).tolist()
        }
        self.client.post('/predict', json=payload)


class PredictLocust(HttpLocust):
    task_set = PredictTaskSet
    wait_time = between(1, 3)
