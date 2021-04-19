import tensorflow as tf
from tensorflow.python.client import device_lib
import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

print(device_lib.list_local_devices())