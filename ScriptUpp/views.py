# coding=utf-8
import os
import uuid
import file_to_modify  # 转码模块
import sqlcheck  # SQL检查模块
import sqlplan   # 执行任务相关
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from SysConfig import config
from DbRegister import views as db_register_view

# Create your views here.


def index(request):
    user_id = request.session['user_id']
    if user_id is None:
        return HttpResponseRedirect('/')
    else:
        print user_id
    return render(request, "ScriptUpp/Base.html")


def exec_sql(request):
    # request method 检测
    if request.method == 'POST':
        sql_files = request.FILES.getlist('sqlFiles')
        ip = request.POST['exec_ip']
        account = request.POST['exec_account']
        databases = request.POST.getlist('exec_db')

        # 读取配置文件
        conf = config.Configer()
        # 获取用户IP
        action_ip = db_register_view.get_action_ip(request)

        # 检测脚本存放路径
        if not os.path.exists(conf.get_script_path()):
            # 不存在则创建脚本路径
            print "SCRIPT_PATH is not existed. Create"

            try:
                os.mkdir(conf.get_script_path())
            except Exception, e:
                # 创建失败返回错误
                s = "Create SCRIPT_PATH error.<br>" + str(e)
                return HttpResponse(s)

        # 错误队列
        all_error_info = []
        # 审核脚本内容
        for sql_file in sql_files:
            check_result = sqlcheck.check_sql_content(sql_file)
            if not check_result['result']:
                all_error_info.append({'errorInfo': check_result['error'], 'fileName': sql_file.name})

        # 无错误信息则落地文本
        if all_error_info.__len__() == 0:
            # 为脚本生成一个基于时间戳+随机数的UUID目录
            script_path = os.path.join(conf.get_script_path(), str(action_ip).replace('.', '_') +
                                       '_' + str(uuid.uuid1()).replace('-', ''))
            # 如果就是巧了重复，那就再随一个，随到没有重复为止
            while os.path.exists(script_path):
                script_path = os.path.join(conf.get_script_path(), str(action_ip).replace('.', '_') +
                                           '_' + str(uuid.uuid1()).replace('-', ''))
            # 创建脚本存放目录
            try:
                os.mkdir(script_path)
            except Exception, e:
                s = u'创建目录%s失败，错误详情：%S' % (script_path, e)
                return HttpResponse(s)

            # 脚本落盘
            for f in sql_files:
                file_to_modify.save_file_to_disk(f, os.path.join(script_path, f.name))

            # 将script_path下的所有文件编码转换成utf8
            file_to_modify.change_file_to_utf8(script_path)
            # 将script_path下的脚本去除USE
            file_to_modify.remove_use(script_path)

            # 生成执行计划
            owner_id = request.session['user_id']
            for db_name in databases:
                sqlplan.init_exec_plan(action_ip, ip, db_name, account, script_path, owner_id)

            for db_name in databases:
                sqlplan.exec_exec_plan(action_ip, ip, db_name, account, script_path)

            return HttpResponseRedirect('/welcome')

        else:
            return HttpResponse(all_error_info)

    # 非POST请求跳回主页面
    else:
        return render(request, "ScriptUpp/Base.html")
