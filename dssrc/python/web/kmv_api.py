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


def set_gpu_mem():
    gpus = tf.config.experimental.list_physical_devices('GPU')
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


def set_param(msg):
    model_input = trans_param("61334", "null", "null", 20, 20, "705", "10NP010", 40, "1", 1, "null", "3_1", "630022", -1, 20, 20, 100)
    return model_input


def get_model(model_loc):

    return keras.models.load_model(model_loc, compile=True)


def get_predict(model, model_input):
    output = model.predict(model_input.reshape(1, -1))
    return np.sign(output[0][0])*(np.exp(np.abs(output[0][0])*10)-1)


def trans_param(rps_pd_cd, py_exem_tp_cd, lwrt_tmn_rfd_tp_cd, ctr_ins_prd, ctr_py_prd, fee_pay_tp_cd, rcrt_bch_org_cd,
                sbc_age, gndr_cd, injr_gr_num, plan_cd, inspe_grde_val,
                cov_cd, sbc_amt, ins_prd, py_prd, rnwl_ed_age):

    pd_dict = {}
    exem_dict = {}
    lwrt_dict = {}
    fee_dict = {}
    pl_dict = {}
    ch_dict = {}
    cov_dict = {}

    with open("/application/mds/dssrc/data/params/pd_dict", "rb") as lf:
        pd_dict = pickle.load(lf)
    with open("/application/mds/dssrc/data/params/exem_dict", "rb") as lf:
        exem_dict = pickle.load(lf)
    with open("/application/mds/dssrc/data/params/lwrt_dict", "rb") as lf:
        lwrt_dict = pickle.load(lf)
    with open("/application/mds/dssrc/data/params/fee_dict", "rb") as lf:
        fee_dict = pickle.load(lf)
    with open("/application/mds/dssrc/data/params/pl_dict", "rb") as lf:
        pl_dict = pickle.load(lf)
    with open("/application/mds/dssrc/data/params/bch_dict", "rb") as lf:
        bch_dict = pickle.load(lf)
    with open("/application/mds/dssrc/data/params/cov_dict", "rb") as lf:
        cov_dict = pickle.load(lf)

    ret = np.zeros(970)

    curIndex = 0

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
    ret[curIndex], ret[curIndex + 1] = ctr_py_prd / 100., ctr_ins_prd / 100.
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
    ret[curIndex] = sbc_age / 100.
    curIndex += 1

    # 성별
    if gndr_cd == '1':
        ret[curIndex] = 1
    elif gndr_cd == '2':
        ret[curIndex + 1] = 1

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

    return ret