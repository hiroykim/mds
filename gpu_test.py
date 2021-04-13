from tensorflow.python.client import device_lib
from tensorflow.python import test
import tensorflow as tf

print(device_lib.list_local_devices())
print(test.is_built_with_cuda())

print(tf.test.is_gpu_available())
