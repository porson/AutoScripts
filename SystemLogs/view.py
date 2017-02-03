# coding:utf8
from django.shortcuts import render
from django.http import HttpResponse
from DbConnecter import dbconnecter
from DbRegister import views as db_reister

import json


def index(request):
    action_ip = db_reister.get_action_ip(request)
    if action_ip == '127.0.0.1':
        return render(request, 'Log/Base.html')
    else:
        return render(request, 'Log/NotPermit.html')


def get_log(request, t):
    action_ip = db_reister.get_action_ip(request)

    connection = dbconnecter.Connection(action_ip)

    if t == 'account':
        sql = "select * from Info_ToolsLog where actiontype in (2,4)"
        info = connection.select_sql(sql)

        logs = []
        for i in info:
            log = {
                'action_ip': i[1],
                'type': i[2],
                'account': i[3],
                'action_time': str(i[5])[:-7]
            }
            logs.append(log)

    elif t == 'databases':
        sql = "select * from Info_ToolsLog where actiontype in (1,3)"
        info = connection.select_sql(sql)

        logs = []
        for i in info:
            log = {
                'action_ip': i[1],
                'type': i[2],
                'database': i[4],
                'action_time': str(i[5])[:-7]
            }
            logs.append(log)

    else:
        sql = "select * from Info_ToolsLog where actiontype in (0,10)"
        info = connection.select_sql(sql)

        logs = []
        for i in info:

            log = {
                'action_ip': i[1],
                'type': i[2],
                'account': i[3],
                'database': i[4],
                'action_time': str(i[5])[:-7]
            }
            logs.append(log)

    logs = json.dumps(logs)
    return HttpResponse(logs)
