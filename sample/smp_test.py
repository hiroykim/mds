
def map_test():
    dt_smpl = {"a" :1, "b" :2, "c" :3}
    lt_smpl = ["a" ,"b" ,"c"]
    lt_smpl2 = [1 ,2 ,3]

    lt_rst = list(map(lambda i: dt_smpl[i], lt_smpl))
    print(lt_rst)

def dict_reverse_test(dt_org):
    dt_new =dict()

    for k, v in dt_org.items():
        print(k, v)
        dt_new[v] =k

    print(dt_new)

def dict_reverse_test2(dt_org):
    dt_new = dict([(v, k) for k, v in dt_org.items()])
    print(dt_new)
    lt_smpl2 = [1, 2, 3, 6]
    lt_new = [dt_new.get(i, "?") for i in lt_smpl2]
    print(lt_new)

if __name__ == "__main__":
    # map_test()
    dt_smpl = {"a": 1, "b": 2, "c": 3}
    dict_reverse_test(dt_smpl)
    dict_reverse_test2(dt_smpl)
