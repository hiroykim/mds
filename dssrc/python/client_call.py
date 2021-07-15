# -*- coding: utf-8 -*-

__author__ = "Meritz"
__date__ = "creation: 2021-03-06, modification: 0000-00-00"


#################
#import
#################
import requests
import json

win=False
cloud=False


def main():

    if win:
        with open("C:\mds\dssrc\data\client\java_kmv_input.json", "r") as fp:
            json_data = json.load(fp)
    else:
        with open("/application/mds/dssrc/data/client/java_kmv_input.json", "r") as fp:
            json_data = json.load(fp)

    if cloud:
        URL="http://221.168.32.244:8080/kmv"
    else:
        URL="http://127.0.0.1:8888/kmv"
    
    # print(json_data)
    # print("type: ", type(json_data))
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    res=requests.post(URL, headers=headers, data=json.dumps(json_data))
    print(res.text)
    print(res.status_code)



if __name__ == "__main__":
    main()
