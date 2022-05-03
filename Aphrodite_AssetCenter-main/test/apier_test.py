# coding=utf-8

import json
import requests
from requests.auth import HTTPBasicAuth

api_path = 'http://127.0.0.1:5000/api'
username = 'apier'
password = 'kbf0JVbDr7TN9xML'


# # get token
def get_token():
    r = requests.get(api_path + '/v1/token', auth=HTTPBasicAuth(username, password))
    token = json.loads(r.content.decode('utf-8'))['token']
    return token


def cve_to_atfield(item_json):
    try:
        token = get_token()
        # 后续新增接口都是使用manager下面的接口，前面的api/v1/asset保留兼容历史
        r = requests.post(api_path + '/cve', auth=HTTPBasicAuth(token, ''), json=item_json)
        if r.status_code == 200 and json.loads(r.content.decode('utf-8')).get('error_code') == 0:
            print('add ok')
        else:
            print('add error')
            print(r.text)
    except Exception as e:
        print(e)   

if __name__ == '__main__':
    cve_item_json = {
        "cve_id": "0001", 
        "cve_name": "00", 
        "cve_status": "0", 
        "cve_time": "2022-03-16", 
        "cve_type": "0"
    }    
    cve_to_atfield(cve_item_json)