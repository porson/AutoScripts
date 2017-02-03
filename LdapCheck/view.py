# coding:utf8
import check_api
import ldap_users
from django.shortcuts import render
from django.http import HttpResponseRedirect
from DbRegister import views as db_register_view


def index(request):
    return render(request, 'index/login.html')


def login(request):
    if request.method == 'POST':
        # 获取账号密码
        user_name = request.POST.get('account')
        password = request.POST.get('password')
        # 获取IP
        action_ip = db_register_view.get_action_ip(request)
        # 域认证
        if check_api.ldap_api(user_name, password):
            # 认证成功在系统内注册用户，更新登录时间
            user_id = ldap_users.login_control(action_ip, user_name)
            # user_id存入session
            request.session['user_id'] = user_id
            return HttpResponseRedirect('/welcome')

        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')