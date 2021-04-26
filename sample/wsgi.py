import os
import numpy as np
from flask import Flask, request
import tensorflow as tf

from build_big_model import build_big_model

model = build_big_model()

app = Flask(__name__)
#os.environ["CUDA_VISIBLE_DEVICES"]="0"

def set_gpu_mem():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)


@app.route('/predict', methods=['POST'])
def predict():
    set_gpu_mem()
    received_input = np.array(request.json['input'])
    model_output = model.predict(received_input)

    return {'predictions': model_output.tolist()}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
