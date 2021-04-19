# -*- coding: utf-8 -*-

__author__ = "Meritz"
__date__ = "creation: 2021-03-06, modification: 0000-00-00"


#################
#import
#################
from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from web import test_model


app = Flask(__name__)
CORS(app)
api = Api(app)


#################
#Class
#################
class KmvApi(Resource):


    @staticmethod
    def mkmsg(param):
        msg = test_model.test_hello()
        return "Hello functions " + str(msg) + str(param)


    @staticmethod
    def get():
        param = request.values.get("msg")
        return {"res" : KmvApi.mkmsg(param)}


    @staticmethod
    def post():
        param = request.values.get("msg")
        return {"res" : KmvApi.mkmsg(param)}


api.add_resource(KmvApi, "/kmv")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host='0.0.0.0',port=8888)
    
