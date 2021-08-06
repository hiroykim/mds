# -*- coding: utf-8 -*-

__author__ = "Meritz"
__date__ = "creation: 2021-03-06, modification: 0000-00-00"


#################
#import
#################
import requests
import json
import zlib
import base64

win=False
cloud=False
DEBUG=False

def main():

    if win:
        with open("C:\mds\dssrc\data\client\java_kmv_input.json", "r") as fp:
            json_data = json.load(fp)

    else:
        with open("/application/mds/dssrc/data/client/java_kmv_input.json", "r") as fp:
            json_data = json.load(fp)

    compress_data = zlib.compress(json.dumps(json_data).encode(encoding='utf-8'), level=9)
    base64_en = base64.b64encode(compress_data)
    if DEBUG:
        print(compress_data)
        print("======================================================")
        print(base64_en)

    #compress_data = base64.b64decode(base64_en)
    #json_data = json.loads(zlib.decompress(compress_data))

    #json_data = {"data_enc" : compress_data}
    #print(json_data)

    if cloud:
        URL="http://221.168.32.244:8080/kmv"
    else:
        URL="http://127.0.0.1:8888/kmv"
    
    # print(json_data)
    # print("type: ", type(json_data))
    #headers = {'Content-Type': 'application/json; charset=utf-8'}
    #res=requests.post(URL, headers=headers, data=json.dumps(json_data))

    data={'json_enc': base64_en}
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
    res=requests.post(URL, headers=headers, data=data)
    #res=requests.get(URL)

    if(res.status_code == 200):
        compress_data = base64.b64decode(res.text)
        json_data = zlib.decompress(compress_data).decode('utf-8')
        print("======================================================")
        print(json.loads(json_data))
        print("======================================================")
        print(res.status_code)
        print("======================================================")
    else:
        print("======================================================")
        print(res.text)
        print("======================================================")
        print(res.status_code)
        print("======================================================")


if __name__ == "__main__":
    main()
