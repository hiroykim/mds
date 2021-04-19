# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import calendar
import copy
import time
import ast
import pickle

import tensorflow as tf
from tensorflow import keras


def trans_param(rps_pd_cd, py_exem_tp_cd, lwrt_tmn_rfd_tp_cd, ctr_ins_prd, ctr_py_prd, fee_pay_tp_cd, rcrt_bch_org_cd, 
                sbc_age, gndr_cd, injr_gr_num, plan_cd, inspe_grde_val, 
                cov_cd, sbc_amt, ins_prd, py_prd, rnwl_ed_age):


    # 제플린에서부터 dict로 만들어 write해두도록 함
    # 이쪽은 서버 특이적으로 어디 달아둬야할 변수들이나 일단 여기서 해둠
    pd_dict = {}
    exem_dict = {}
    lwrt_dict = {}
    fee_dict = {}
    pl_dict = {}
    ch_dict = {}
    cov_dict = {}

    with open("/home/hdpapp/deployment/mds/dssrc/data/params/pd_dict", "rb") as lf:
        pd_dict = pickle.load(lf)
    with open("/home/hdpapp/deployment/mds/dssrc/data/params/exem_dict", "rb") as lf:
        exem_dict = pickle.load(lf)
    with open("/home/hdpapp/deployment/mds/dssrc/data/params/lwrt_dict", "rb") as lf:
        lwrt_dict = pickle.load(lf)
    with open("/home/hdpapp/deployment/mds/dssrc/data/params/fee_dict", "rb") as lf:
        fee_dict = pickle.load(lf)
    with open("/home/hdpapp/deployment/mds/dssrc/data/params/pl_dict", "rb") as lf:
        pl_dict = pickle.load(lf)
    with open("/home/hdpapp/deployment/mds/dssrc/data/params/bch_dict", "rb") as lf:
        bch_dict = pickle.load(lf)
    with open("/home/hdpapp/deployment/mds/dssrc/data/params/cov_dict", "rb") as lf:
        cov_dict = pickle.load(lf)

    #featuer 
    #참고: java ...model.java의 xxxx를 보세요
    #참고: pyspahr..무슨선스 무슨 소스이 어느 함수보세요..

    # 970은 ModelInfo.java의 input_len과 같음. 모형배포때마다 다를 수 있음. 
    ret = np.zeros(970)

    curIndex = 0

    # list 데이터는 모형을 만들때 parquet로 내려두었고, 이를 zeppelin에서 읽어 pickle 통해 파일로 내려두고 여기서 read해와야함
    # list 를 내려서 for loop 돌릴게 아니라 그냥 dictionary로 만들어놓고 인덱스를 바로 찍는게 효율적

    # 상품코드 one-hot
    #for cd in pd_list:
    #    if cd==rps_pd_cd:
    #        feature.append(1.)
    #    else:
    #        feature.append(0.) 

    # 상품코드
    if rps_pd_cd in pd_dict:
        ret[curIndex + pd_dict[rps_pd_cd]] = 1
    curIndex += len(pd_dict)

    # 납입면제유형코드
    if py_exem_tp_cd in exem_dict: 
        ret[curIndex + exem_dict[py_exem_tp_cd]] = 1
    curIndex += len(exem_dict)

    # 저율해지유형코드
    if lwrt_tmn_rfd_tp_cd in lwrt_dict: 
        ret[curIndex + exem_dict[lwrt_tmn_rfd_tp_cd]] = 1
    curIndex += len(lwrt_dict)

    # 계약의 보험기간 / 납입기간
    ret[curIndex], ret[curIndex+1] = ctr_py_prd/100., ctr_ins_prd/100.
    curIndex += 2

    # 수수료지급유형코드
    if fee_pay_tp_cd in fee_dict:
        ret[curIndex + fee_dict[fee_pay_tp_cd]] = 1
    curIndex += len(fee_dict)

    # 모집조직
    if rcrt_bch_org_cd in bch_dict:
        ret[curIndex + bch_dict[rcrt_bch_org_cd]] = 1
    curIndex += len(bch_dict)

    # 연령
    ret[curIndex] = sbc_age/100.
    curIndex += 1

    # 성별
    if gndr_cd == '1':
        ret[curIndex] = 1
    elif gndr_cd == '2':
        ret[curIndex+1] = 1

    curIndex += 2

    # 직업급수
    if 1 <= injr_gr_num <= 3:
        ret[curIndex + injr_gr_num - 1] = 1
    curIndex += 3

    # 플랜코드
    if plan_cd in pl_dict:
        ret[curIndex + pl_dict[plan_cd]] = 1
    curIndex += len(pl_dict)

    # 상해등급
    if inspe_grde_val is not None:
        grde = int(inspe_grde_val[0])
        if 1 <= grde <= 3:
            ret[curIndex + grde - 1] = 1
    curIndex += 3

    # 한줄 eval은 거의 이와 비슷한 형태로 이어집니다.
    # 담보코드(cov_list) 관련된 쪽은 유의하게 다릅니다. 
    # 이쪽은 추가 코멘트 남기겠습니다

    # 담보코드
    if cov_cd in cov_dict:
        ret[curIndex + cov_dict[cov_cd][0]] = 1
    curIndex += len(cov_dict)

    if cov_cd in cov_dict:
        input_val = 0
        if cov_dict[cov_cd][1] <= 0:
            input_val = 1
        elif sbc_amt >= 0:
            input_val = np.min([1.0, sbc_amt / cov_dict[cov_cd][1]])
        else:
            input_val = cov_dict[cov_cd][2] / cov_dict[cov_cd][1]
        ret[curIndex + cov_dict[cov_cd][0]] = input_val
    curIndex += len(cov_dict)


    # 여러줄 한번에 eval은 970size 어레이가 아닌 (상품내담보코드수, 970)shape 매트릭스여야 됩니다.
    # 담보코드 전까지 나오는 각종 코드값들의 경우, 하나의 설계 내에서 같은 값들일 것이기에(상품코드, 납면코드, 연령 등)
    # 한줄 eval한 결과를 replicate하는 방식으로 자바에서는 처리했었습니다
    # (Test.java의 makeInputAllSample())
    
    # 파이썬에서는 numpy matrix 의 특정 col 에 한 값을 어싸인하는 식으로 처리하는게 낫지 싶습니다.
    # ex) 한줄 때: ret[curIndex + pd_dict[rps_pd_cd]] = 1 
    #     여러줄 : retMatrix[:, curIndex + pd_dict[rps_pd_cd]] = 1

    print_sparse(ret)

    return ret


def print_sparse(arr):

    i = -1
    for val in arr:
        i += 1
        if val != 0:
            print(str(i) + ": " + str(val))


# 한 줄에 대한 요청처리함수인지 여러 줄에 대한 요청처리함수인지 이걸 나눌지 합칠지 등은 좀더 고민필요합니다.
# 한줄이다 생각하고 일단 플로우만 완성해둬볼게요
def call_model(modelInput):
    
    #v = lad*(hd5., afajk)
    
    #ex 값이 뭐뭐가 나오면 맞는거예요..
    #print(v)

    # 배포된모델로 바꿔야되고 대충 이렇게 로드하는데, model 로드는 서비스 시작때 한번만 이루어져야 하지만
    # 일단 그냥 여기서 로드
    #model = keras.models.load_model('/home/hdpapp/JM/KMV_prediction_v2021030201_1031_0.0006_0.0005.h5', compile=True)
    model = keras.models.load_model('/home/hdpapp/deployment/mds/dssrc/data/model/KMV_prediction_v2021030201_1031_0.0006_0.0005.h5', compile=True)

    # 모델에 인풋을 넣어 결과값을 받는 장면
    output = model.predict(modelInput.reshape(1, -1))

    # 모형 결과를 환산율로 변환하는 코드입니다.
    kmv_predict = np.sign(output[0][0])*(np.exp(np.abs(output[0][0])*10)-1)

    return kmv_predict


def test_call(msg):
    return msg
    

#def kmv_model(param):
def kmv_model():

    #1. 파라미터 변환
    #json형태로 왔던 파라미터 -> 딕셔너리 형태 -> trans_param 인풋
    #msg = trans_param(param)

    # zeppelin 노트의 _make_feature, Test.java의 makeInputSample 함수 참고
    modelInput = trans_param("61334", "null", "null", 20, 20, "705", "10NP010", 40, "1", 1, "null", "3_1", "630022", -1, 20, 20, 100)
    

    msg = call_model(modelInput)
#    msg = 1

    return msg 


if __name__ == "__main__":
    gpus = tf.config.experimental.list_physical_devices('GPU')
    '''
    if gpus:
        try:
            tf.config.experimental.set_memory_growth(gpus[0], True)
        except RuntimeError as e:
            # 프로그램 시작시에 메모리 증가가 설정되어야만 합니다
            print(e)
    '''
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)

    kmv_model()
