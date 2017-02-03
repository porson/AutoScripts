# coding:utf8
from django.shortcuts import render
from DbConnecter import dbconnecter
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def index(request):
    return render(request, 'DbRegister/Base.html')


# Get connection ip
def get_action_ip(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        action_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        action_ip = request.META['REMOTE_ADDR']
    return action_ip


def register(request):
    if request.method == 'POST':

        action_ip = get_action_ip(request)
        print action_ip

        connection = dbconnecter.Connection(action_ip)

        if request.POST.has_key('account'):
            account = request.POST['account']
            password = request.POST['password']
            ip = request.POST['ip']
            account_info = request.POST['accountInfo']

            hash_password = dbconnecter.password_encoding(password)

            if connection.account_validate(ip, account):
                connection.create_user(ip, account, hash_password, account_info)
                return render(request, 'DbRegister/Base.html')
            else:
                return HttpResponse('账号已经存在')

        else:
            ip = request.POST['ip']
            db_name = request.POST['dbName']
            db_info = request.POST['dbinfo']

            if connection.database_validate(ip, db_name):
                connection.create_database(ip, db_name, db_info)
                return HttpResponseRedirect('/welcome')
            else:
                return HttpResponse('数据库已经存在')

    else:
        return HttpResponseRedirect('/welcome')
