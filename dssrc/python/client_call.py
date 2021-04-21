# -*- coding: utf-8 -*-

__author__ = "Meritz"
__date__ = "creation: 2021-03-06, modification: 0000-00-00"


#################
#import
#################
from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from web import kmv_api
import os
import requests
import json


def main():

    with open("/application/mds/dssrc/data/client/java_kmv_input.json", "r") as fp:
        # dict
        json_data = json.load(fp)



if __name__ == "__main__":
    main()