from tensorflow.python.client import device_lib
from tensorflow.python import test

print(device_lib.list_local_devices())
print(test.is_built_with_cuda())