# coding=utf-8

import json
import requests
from requests.auth import HTTPBasicAuth

api_path = 'http://10.107.120.2:8080/api/v1'
username = 'apier'
password = 'kbf0JVbDr7TN9xML'
# get token
r = requests.get(api_path + '/token', auth=HTTPBasicAuth(username, password))
token = json.loads(r.content.decode('utf-8'))['token']
print(token)

def deleteInnerHost():
    # get old ip
    r = requests.get(api_path + '/asset/innerhost?pageNo=1&pageSize=10000', auth=HTTPBasicAuth(token, ''))
    # print(r.content)
    delete_ip_list = [item['ip'] for item in json.loads(r.content.decode('utf-8')).get('msg').get('items')]
    print(delete_ip_list)
    
    # delete ip
    r = requests.post(api_path + '/asset/innerhost/batch', auth=HTTPBasicAuth(token, ''),
                      json={'action': 'delete', 'info': delete_ip_list})
    if r.status_code != 204:
        print('delete ip err')
    else:
        print('delete ip ok')    


def deleteService():
    # get old 
    r = requests.get(api_path + '/asset/service?pageNo=1&pageSize=10000', auth=HTTPBasicAuth(token, ''))
    # print(r.content)
    delete_service_uid_list = [item['uid'] for item in json.loads(r.content.decode('utf-8')).get('msg').get('items')]

    # delete 
    r = requests.post(api_path + '/asset/service/batch', auth=HTTPBasicAuth(token, ''),
                      json={'action': 'delete', 'info': delete_service_uid_list})
    if r.status_code != 204:
        print('delete servcie err')
    else:
        print('delete servcie ok')    

if __name__ == '__main__':
    # deleteInnerHost()
    deleteService()
