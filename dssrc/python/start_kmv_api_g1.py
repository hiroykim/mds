# -*- coding: utf-8 -*-

__author__ = "Meritz"
__date__ = "creation: 2021-03-06, modification: 0000-00-00"

#################
# import
#################
from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from web import kmv_api
import os
import time

app = Flask(__name__)
CORS(app)
api = Api(app)

# gpu 0,1
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

model_loc = '/application/mds/dssrc/data/model/KMV_prediction_v2021030201_1031_0.0006_0.0005.h5'
kmv_api.set_gpu_mem()
model = kmv_api.get_model(model_loc)
dt_pickle = kmv_api.load_pickle()

'''
@app.before_first_request
def before_first_request():
    global model
    kmv_api.set_gpu_mem()
    model = kmv_api.get_model(model_loc)
'''


#################
# Class
#################
class KmvApi(Resource):

    @staticmethod
    def mkmsg(data):
        rows = len(data.get("lgtmPdCovErnRtMngMdelCovInpCoVo"))
        model_input = kmv_api.set_data(dt_pickle, data, rows)
        np_out, np_out2 = kmv_api.get_predict(model, model_input, rows)

        lt_rst = list()
        lt_cov = data.get("lgtmPdCovErnRtMngMdelCovInpCoVo")
        i = 0
        for dt_cov in lt_cov:
            dt_rst = dict()
            dt_rst["covCd"] = dt_cov.get("covCd")
            dt_rst["mdelPcsRsl"] = str(np_out[i][0])
            dt_rst["ernRt"] = str(np_out2[i][0])
            lt_rst.append(dt_rst)
            i += 1

        return lt_rst

    @staticmethod
    def get():
        data = request.get_json(silent=True)
        return {"res": KmvApi.mkmsg(data)}

    @staticmethod
    def post():

        st_time = time.time()
        data = request.get_json(silent=True)
        # print("header :", request.headers)
        # print("data : ", data)
        ret = KmvApi.mkmsg(data)
        print("gab : ", time.time() - st_time)
        return {"res": ret}


api.add_resource(KmvApi, "/kmv")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=8111)

# curl -iX POST 'http://127.0.0.1:8111/kmv' -H 'Content-Type:application/json' -d '{"param":"test"}'
