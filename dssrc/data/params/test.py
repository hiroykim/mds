import tensorflow as tf
from tensorflow import keras
import pickle

#model_best = keras.models.load_model('/home/hdpapp/JM/KMV_prediction_v2021030201_1031_0.0006_0.0005.h5', compile=True)

pd_list = []
cov_list = [] 
fee_list = [] 
pl_list = []
bch_list = [] 
exem_list = []
lwrt_list = []

with open("/home/hdpapp/yktest/python_test/pd_list", "rb") as lf:
	pd_list = pickle.load(lf)

print(pd_list)
