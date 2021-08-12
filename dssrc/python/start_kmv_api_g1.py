# -*- coding: utf-8 -*-

__author__ = "Meritz"
__date__ = "creation: 2021-03-06, modification: 0000-00-00"

#################
# import
#################
from flask import Flask, request, make_response
from flask_restful import Api, Resource
from flask_cors import CORS
from web import kmv_api
import os
import time
import zlib
import base64
import json
import traceback
import socket
import pickle


app = Flask(__name__)
CORS(app)
api = Api(app)

# gpu 0,1
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

#model_loc = '/application/mds/dssrc/data/model/KMV_prediction_v2021030201_1031_0.0006_0.0005.h5'
model_loc = '/application/mds/dssrc/data/model/KMV_model.h5'
kmv_api.set_gpu_mem()
model = kmv_api.get_model(model_loc)
dt_pickle = kmv_api.load_pickle()

with open("/application/mds/dssrc/data/params/whitelist", "rb") as lf:
    wh_set = pickle.load(lf)


'''
@app.before_first_request
def before_first_request():
    global model
    kmv_api.set_gpu_mem()
    model = kmv_api.get_model(model_loc)
'''

# flask-apm
import logging
from elasticapm.contrib.flask import ElasticAPM
from elasticapm.handlers.logging import Formatter

if socket.gethostname().startswith("vm-gpu"):
    APM_URL='http://192.168.255.72:8200'
else:
    APM_URL='http://127.0.0.1:8200'

app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'kmv_apm',
    #'SERVER_URL': 'http://192.168.255.72:8200',
    #'SERVER_URL': 'http://127.0.0.1:8200',
    'SERVER_URL': APM_URL,
    # 'SECRET_TOKEN': ''
   'DEBUG': False
}

apm = ElasticAPM(app, logging=logging.WARNING)
#apm = ElasticAPM(app, logging=logging.INFO)
#apm = ElasticAPM(app, logging=logging.DEBUG)
fh = logging.FileHandler('kmv_apm.log')
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logging.getLogger().addHandler(fh)

DEBUG=False

#################
# Class
#################
class KmvApi(Resource):

    @staticmethod
    def mkmsg(json_enc):
        try:
            compress_data = base64.b64decode(json_enc)
            json_str = zlib.decompress(compress_data).decode('utf-8')
            data = json.loads(json_str)
            if DEBUG:
                print("compress_data : ", compress_data)
                print("data : ", json_str)

            rows = len(data.get("lgtmPdCovErnRtMngMdelCovInpCoVo",""))
            model_input = kmv_api.set_data(dt_pickle, data, rows)
            np_out, np_out2 = kmv_api.get_predict(model, model_input, rows)

            lt_rst = list()
            lt_cov = data.get("lgtmPdCovErnRtMngMdelCovInpCoVo")
            i = 0
            if len(data.get("sbcAge","")) == 2:
                age_str = "0"+ data.get("sbcAge")[0] + "0"
            elif len(data.get("sbcAge","")) == 3:
                age_str = data.get("sbcAge")[0:2] + "0"
            else:
                age_str = "000"
            for dt_cov in lt_cov:
                dt_rst = dict()
                dt_rst["covCd"] = dt_cov.get("covCd")
                dt_rst["mdelPcsRsl"] = str(np_out[i][0])
                dt_rst["ernRt"] = str(np_out2[i][0])
                key_str = data.get("rpsPdCd") + dt_cov.get("covCd") + data.get("gndrCd") + age_str
                #print(key_str)
                dt_rst["flg"] = 1 if key_str in wh_set else 0
                lt_rst.append(dt_rst)
                i += 1

            #raise Exception("Test")
            return lt_rst
        except Exception:
            apm.capture_exception()
            apm.capture_message("APM Error - mkmsg Error")
            raise Exception(traceback.format_exc())
            return "mkmsg Error is Occured"

    @staticmethod
    def get():
        json_enc = request.values.get("json_enc", "No data")
        # data = request.get_json(silent=True)

        if DEBUG:
            st_time = time.time()
            print("request :", request)
            print("header :", request.headers)
            print("data : ", json_enc)

        ret = KmvApi.mkmsg(json_enc)
        compress_data = zlib.compress(json.dumps(ret).encode(encoding='utf-8'))
        base64_en = base64.b64encode(compress_data)
        response = make_response(base64_en)
        if DEBUG:
            print("gab : ", time.time() - st_time)
        return response

    @staticmethod
    def post():
        json_enc = request.values.get("json_enc")
        # data = request.get_json(silent=True)

        if DEBUG:
            st_time = time.time()
            print("request :", request)
            print("header:", request.headers)
            print("param:", request.values)
            print("data : ", json_enc)
        
        try:
            ret = KmvApi.mkmsg(json_enc)
            compress_data = zlib.compress(json.dumps({"res":ret}).encode(encoding='utf-8'),level=9)
            base64_en = base64.b64encode(compress_data)
            response = make_response(base64_en)
            if DEBUG:
                print("gab : ", time.time() - st_time)
            return response
        except Exception:
            return make_response(traceback.format_exc(), 500)

api.add_resource(KmvApi, "/kmv")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=8888)
 
# curl -iX POST 'http://127.0.0.1:8111/kmv' -H 'Content-Type:application/json' -d '{"param":"test"}'
