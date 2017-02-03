# coding:utf8
import json

from DbConnecter import dbconnecter
from DbRegister import views as db_reister
from django.http import HttpResponse


def get_accounts(request):
    action_ip = db_reister.get_action_ip(request)
    connection = dbconnecter.Connection(action_ip)

    sql = "select ip,account,info from Info_DbAccount"
    infos = connection.select_sql(sql)

    accounts = []
    for i in infos:
        account_info = {
            'ip': i[0],
            'account': i[1],
            'info': i[2]
        }
        accounts.append(account_info)

    result = json.dumps(accounts)

    return HttpResponse(result)


def get_databases(request):
    action_ip = db_reister.get_action_ip(request)
    connection = dbconnecter.Connection(action_ip)

    sql = "select ip,dbname,info from Info_DatabaseInfo"
    infos = connection.select_sql(sql)

    databases = []
    for i in infos:
        database_info = {
            'ip': i[0],
            'dbname': i[1],
            'info': i[2]
        }
        databases.append(database_info)

    result = json.dumps(databases)

    return HttpResponse(result)


def get_ip_from_db(request):
    action_ip = db_reister.get_action_ip(request)
    connection = dbconnecter.Connection(action_ip)

    sql = "SELECT DISTINCT IP FROM Info_DatabaseInfo"
    infos = connection.select_sql(sql)
    result = json.dumps(infos)
    return HttpResponse(result)


def get_databases_with_ip(request, ip):
    action_ip = db_reister.get_action_ip(request)
    connection = dbconnecter.Connection(action_ip)

    sql = "select dbname from Info_DatabaseInfo where ip = '%s'" % ip
    infos = connection.select_sql(sql)

    result = json.dumps(infos)

    return HttpResponse(result)


def get_account_with_ip(request, ip):
    action_ip = db_reister.get_action_ip(request)
    connection = dbconnecter.Connection(action_ip)

    sql = "select account from Info_DbAccount where ip = '%s'" % ip
    infos = connection.select_sql(sql)

    result = json.dumps(infos)

    return HttpResponse(result)