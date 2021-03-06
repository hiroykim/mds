# -*- coding: utf-8 -*-

import numpy as np
import pickle
import json

import tensorflow as tf
from tensorflow import keras
import os


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


def parse_comm(dt_pickle, data, rows):
    cols = dt_pickle["com_cols"]
    ret = np.zeros((rows, cols))
    curIndex = 0

    # 상품코드 len(dt_pickle.get("pd_dict"))
    pd_dict = dt_pickle.get("pd_dict")
    rps_pd_cd = data.get("rpsPdCd")
    if rps_pd_cd in pd_dict:
        ret[:, curIndex + pd_dict[rps_pd_cd]] = 1
    curIndex += len(pd_dict)

    # 납입면제유형코드 len(dt_pickle.get("exem_dict"))
    exem_dict = dt_pickle.get("exem_dict")
    py_exem_tp_cd = data.get("pyExemTpCd")
    if py_exem_tp_cd in exem_dict:
        ret[:, curIndex + exem_dict[py_exem_tp_cd]] = 1
    curIndex += len(exem_dict)

    # 저율해지유형코드 len(dt_pickle.get("lwrt_dict"))
    lwrt_dict = dt_pickle.get("lwrt_dict")
    lwrt_tmn_rfd_tp_cd = data.get("lwrtTmnRfdTpCd")
    if lwrt_tmn_rfd_tp_cd in lwrt_dict:
        ret[:, curIndex + lwrt_dict[lwrt_tmn_rfd_tp_cd]] = 1
    curIndex += len(lwrt_dict)

    # check!!
    # 계약의 보험기간 / 납입기간 2
    ctr_py_prd = float(data.get("ctrPyPrd",0))
    ctr_ins_prd = float(data.get("ctrInsPrd",0))
    ret[:, curIndex], ret[:, curIndex+1] = ctr_py_prd/100., ctr_ins_prd/100.
    curIndex += 2

    # 수수료지급유형코드 len(dt_pickle.get("fee_dict"))
    fee_dict = dt_pickle.get("fee_dict")
    fee_pay_tp_cd = data.get("feePayTpCd")
    if fee_pay_tp_cd in fee_dict:
        ret[:, curIndex + fee_dict[fee_pay_tp_cd]] = 1
    curIndex += len(fee_dict)

    # 모집조직 len(dt_pickle.get("bch_dict"))
    bch_dict = dt_pickle.get("bch_dict")
    rcrt_bch_org_cd = data.get("rcrtOrgCd")
    if rcrt_bch_org_cd in bch_dict:
        ret[:, curIndex + bch_dict[rcrt_bch_org_cd]] = 1
    curIndex += len(bch_dict)

    # check!!
    # 연령 1
    sbc_age = float(data.get("sbcAge",0))
    ret[:, curIndex] = sbc_age/100.
    curIndex += 1

    # 성별 2
    gndr_cd = data.get("gndrCd")
    if gndr_cd == '1':
        ret[:, curIndex] = 1
    elif gndr_cd == '2':
        ret[:, curIndex+1] = 1

    curIndex += 2

    # check!!
    # 직업급수 3
    job_gr_num = data.get("jobGrd","1")
    if job_gr_num.isdigit():
        job_gr_num = int(job_gr_num)
    else:
        job_gr_num =1
    if 1 <= job_gr_num <= 3:
        ret[:, curIndex + job_gr_num - 1] = 1
    curIndex += 3

    # 플랜코드 len(dt_pickle.get("pl_dict"))
    pl_dict = dt_pickle.get("pl_dict")
    plan_cd = data.get("planCd")
    if plan_cd in pl_dict:
        ret[:, curIndex + pl_dict[plan_cd]] = 1
    curIndex += len(pl_dict)

    # check!!
    # 상해등급 3
    injr_gr_num = data.get("injrGrde","0")
    if injr_gr_num.isdigit():
        grde = int(injr_gr_num)
    else:
        grde = 0
    if 1 <= grde <= 3:
        ret[:, curIndex + grde - 1] = 1

    return ret


def parse_cov(dt_pickle, data, rows):
    cols = dt_pickle["cov_cols"]
    cov_dict = dt_pickle.get("cov_dict")
    sbc_amt = -1
    ret = np.zeros((rows,cols))
    curIndex = 0
    # 담보코드
    cur_rows = 0
    lt_cov = data.get("lgtmPdCovErnRtMngMdelCovInpCoVo")
    for dt_cov in lt_cov:
        cov_cd = dt_cov["covCd"]
        if cov_cd in cov_dict:
            ret[cur_rows , cov_dict[cov_cd][0]] = 1
        curIndex += len(cov_dict)

        if cov_cd in cov_dict:
            if cov_dict[cov_cd][1] <= 0:
                input_val = 1
            elif sbc_amt >= 0:
                input_val = np.min([1.0, sbc_amt / cov_dict[cov_cd][1]])
            else:
                input_val = cov_dict[cov_cd][2] / cov_dict[cov_cd][1]
            ret[cur_rows, curIndex + cov_dict[cov_cd][0]] = input_val
   
        curIndex += len(cov_dict)
        ins_prd = dt_cov["insPrd"]
        py_prd = dt_cov["pyPrd"]
        rnwl_ed_age = dt_cov["rnwlEdAge"]
        ret[cur_rows, curIndex] = ins_prd/100.
        ret[cur_rows, curIndex + 1] = py_prd/100.
        ret[cur_rows, curIndex + 2] = rnwl_ed_age/100.
        
        curIndex = 0
        cur_rows += 1 


    return ret


def set_data(dt_pickle, data, rows):

    # print("rows: ", rows)
    comm_input = parse_comm(dt_pickle, data, rows)
    cov_input = parse_cov(dt_pickle, data, rows)

    return np.concatenate((comm_input, cov_input), axis=1)


def get_model(model_loc):
    return keras.models.load_model(model_loc, compile=True)


def load_pickle():
    dt_pickle = {}

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

    dt_pickle["pd_dict"] = pd_dict
    dt_pickle["exem_dict"] = exem_dict
    dt_pickle["lwrt_dict"] = lwrt_dict
    dt_pickle["fee_dict"] = fee_dict
    dt_pickle["pl_dict"] = pl_dict
    dt_pickle["bch_dict"] = bch_dict
    dt_pickle["cov_dict"] = cov_dict
    
    com_cols = len(dt_pickle.get("pd_dict")) + len(dt_pickle.get("exem_dict")) + len(dt_pickle.get("lwrt_dict")) \
                + 2 + len(dt_pickle.get("fee_dict")) + len(dt_pickle.get("bch_dict")) + 1 + 2 + 3 \
                + len(dt_pickle.get("pl_dict")) + 3
    cov_cols = len(dt_pickle.get("cov_dict")) * 2 + 3

    dt_pickle["com_cols"] = com_cols
    dt_pickle["cov_cols"] = cov_cols
    tot_cols = com_cols + cov_cols
    dt_pickle["tot_cols"] = tot_cols

    #test
    if 0:
        print("-----------------------")
        print(com_cols, cov_cols, tot_cols)

    return dt_pickle


def get_predict(model, model_input, rows):
    #output = model.predict(model_input.reshape(1, -1))
    output = model.predict(model_input)
    output2 = np.zeros_like(output)
    for i in range(0, rows):
        output2[i][0] = np.sign(output[i][0]) * (np.exp(np.abs(output[i][0]) * 10) - 1)
    return output, output2



##############################
# Test Code
##############################
def main():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    #model_loc = '/application/mds/dssrc/data/model/KMV_prediction_v2021030201_1031_0.0006_0.0005.h5'
    model_loc = '/application/mds/dssrc/data/model/KMV_model.h5'
    set_gpu_mem()
    model = get_model(model_loc)
    dt_pickle = load_pickle()
    with open("/application/mds/dssrc/data/client/java_kmv_input.json", "r") as fp:
        # dict
        json_data = json.load(fp)

    rows = len(json_data.get("lgtmPdCovErnRtMngMdelCovInpCoVo",""))
    model_input = set_data(dt_pickle, json_data, rows)
    print(model_input)
    print(model_input.ndim)
    print(model_input.shape)
    
    np_out, np_out2 = get_predict(model, model_input, rows)
    print(np_out.ndim)
    print(np_out.shape)
    print(np_out2.ndim)
    print(np_out2.shape)
    #print(np_out)

    lt_rst = list()
    lt_cov = json_data.get("lgtmPdCovErnRtMngMdelCovInpCoVo")
    i=0
    for dt_cov in lt_cov:
        dt_rst=dict()
        dt_rst["covCd"] = dt_cov.get("covCd")
        dt_rst["mdelPcsRsl"] = str(np_out[i][0])
        dt_rst["ernRt"] = str(np_out2[i][0])
        lt_rst.append(dt_rst)
        i += 1

    print(lt_rst)

if __name__ == "__main__":
    main()
