import requests
import json
import base64

import sys
import os


def file_to_base64(input_init):
    cont = open(input_init['file_path'], 'rb').read()
    base_cont = base64.b64encode(cont)
    base_cont = base_cont.decode('utf-8')  # if sys.version.startswith('3') else base_cont  # 兼容python2与python3
    input_init['file_base64'] = base_cont

    return input_init


def get_dict_from_path(_path):
    # load json dict from json file
    # output form: dictionary
    # f = open(_path, 'r', encoding='gbk')
    f = open(_path, 'r', encoding='utf-8')
    _dict = json.load(f)
    f.close()
    return _dict


def write_json_from_dict(_dict, _path, simple_write=True):
    with open(_path, 'w') as f_log:
        if simple_write:
            f_log.write(json.dumps(_dict, indent=4, ensure_ascii=False))
        else:
            f_log.write(json.dumps(_dict))

    return _dict


def bert_similarity(root_str, cand_str):
    url = "http://ai03cn.haetek.com:9090/ltp"
    data = {
        "model_name": "bert",
        "model_action": "similarity",
        "extra_data": {
            "root_str": root_str,
            "cand_str": cand_str
        },
        "model_type": ""
    }
    res = requests.post(url=url, json=data)
    return json.loads(res.text)


def search_F(query, max_size=3):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'api_info_2021jan13.json')
    # print(current_dir)
    # print(file_path)
    _dict = get_dict_from_path(file_path)

    key_list = []
    value_list = []
    for _key in _dict:
        key_list.append(_key)
        value_list.append(_dict[_key]['func'])

    res = bert_similarity(query, value_list)['result_data']
    pair_res = [[key_list[_id], res[_id]] for _id in range(len(res))]

    sorted_pair = sorted(pair_res, key=lambda item: item[1], reverse=True)[:max_size]
    res_list = [{'func_name': item[0], 'score': round(item[1], 4), **_dict[item[0]]} for item in sorted_pair]

    return res_list


def run(model_action, user_id, secret_key, input_unit={}, params={}):
    """
    调用服务器接口
    :param model_action: F1/F2/F3/...
    :param user_id: user_sample
    :param secret_key: key_sample
    :param input_unit: 不可为空
    :param params: 可为空
    :return:
    """
    url = 'https://web08cn.haetek.com:9292/api_merger'
    data = {"model_name": "api_merger",
            "model_action": model_action,
            "extra_data": {
                "user_id": user_id,
                "secret_key": secret_key,
                "input_unit": input_unit,
                "params": params
            }
            }
    resp = requests.post(url=url, json=data)
    res_data = json.loads(resp.text)
    # print(res_data)
    return res_data
