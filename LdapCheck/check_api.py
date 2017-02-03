# coding:utf8
import datetime
import json
import time

import requests


def ldap_api(user_name, password):
    """
    域认证
    :param user_name:   域账号
    :param password:    域密码
    :return:
    """
    url = 'http://10.22.2.202/sysopsapi/'
    timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
    data = {

        "jsonrpc": "2.0",
        "method": "ldapcheck.ldapcheck",
        "id": 0,
        "timestamp": timestamp,
        "auth": None,
        "params": {
            "username": user_name,
            "password": password
        }
    }

    r = requests.post(url, data=json.dumps(data))
    print json.loads(r.content)['result']
    if json.loads(r.content)['result']:
        return True
    else:
        return False
