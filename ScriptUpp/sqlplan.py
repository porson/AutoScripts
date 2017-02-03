# coding=utf8
import subprocess
import json
import re
from DbRegister import views as dbregister_views
from django.http import HttpResponse
from DbConnecter import dbconnecter
from SysConfig import config


def get_database_with_id(action_ip, db_id):
    sql = "SELECT [IP],[DbName] FROM [dbo].[Info_DatabaseInfo] where id = '%s'" % db_id
    conn = dbconnecter.Connection(action_ip)
    result = conn.select_sql(sql)[0]
    result = {
        'IP': result[0],
        'DbName': result[1]
              }
    return result


def get_account_with_id(action_ip, acount_id):
    sql = "SELECT [IP],[Account],[Password] FROM [dbo].[Info_DbAccount] where id = '%s'" % acount_id
    conn = dbconnecter.Connection(action_ip)
    result = conn.select_sql(sql)[0]
    result = {
        'IP': result[0],
        'AccountName': result[1],
        'hashPassword': result[2]
              }
    return result


def get_db_id(action_ip, dbname, ip):
    conn = dbconnecter.Connection(action_ip)
    sql = "SELECT [ID] FROM [dbo].[Info_DatabaseInfo] WHERE Dbname = '%s' and IP = '%s' and isActive = 0" % (dbname, ip)
    result = conn.select_sql(sql)
    return result[0][0]


def get_account_id(action_ip, account, ip):
    conn = dbconnecter.Connection(action_ip)
    sql = "SELECT [ID] FROM [dbo].[Info_DbAccount] WHERE account = '%s' and IP = '%s' and isActive = 0" % (account, ip)
    result = conn.select_sql(sql)
    return result[0][0]


def init_exec_plan(action_ip, ip, db_name, account, path, owner_id):
    print u"初始化执行计划"
    # 创建链接
    conn = dbconnecter.Connection(action_ip)
    # 获取账号id
    account_id = get_account_id(action_ip, account, ip)
    # 获取数据库id
    db_id = get_db_id(action_ip, db_name, ip)

    # 查询计划是否存在
    sql = "SELECT [IsDone] FROM [dbo].[Exec_PlanInfo] WHERE dbid = '%s' AND path = '%s'" % (db_id, path)
    result = conn.select_sql(sql)
    # 不存在，则创建任务
    if result.__len__() == 0:
        sql = "INSERT INTO " \
              "[dbo].[Exec_PlanInfo]([IP],[DbID],[AccountID],[Path],[StartTime],[EndTime],[IsDone],[UserID])" \
              "VALUES ('%s','%d','%d','%s',getdate(),'',0,'%d')" % (ip, db_id, account_id, path, owner_id)
        conn.insert_sql(sql)
    else:
        print u'已存在'
        pass


def exec_exec_plan(action_ip, ip, db_name, account, path):
    print u"开始执行.."
    # 获取数据库id
    db_id = get_db_id(action_ip, db_name, ip)
    # 获取账号id
    account_id = get_account_id(action_ip, account, ip)
    account_info = get_account_with_id(action_ip, account_id)
    # 通过账号ID获取解密密码
    password = dbconnecter.password_decoding(account_info['hashPassword'])
    # 从配置文件中获取PowerShell路径
    sh_path = config.Configer().get_shell_path()

    # 创建链接
    conn = dbconnecter.Connection(action_ip)
    # 查找执行计划
    sql = "SELECT [IsDone] FROM [dbo].[Exec_PlanInfo] WHERE ip = '%s' and dbid = %d and path = '%s'" \
          % (ip, db_id, path)
    # 检查执行状态
    result = conn.select_sql(sql)[0][0]
    if not result:
        # 调用PowerShell执行脚本
        args = [r"powershell", sh_path, db_name, ip, path, account, password]
        try:
            p = subprocess.Popen(args, stdout=subprocess.PIPE)
            dt = p.stdout.read()
            print dt
            pattern = r'.*error:.*'
            if not re.match(pattern, dt):
                # 修改执行状态
                sql = "UPDATE [dbo].[Exec_PlanInfo] SET [IsDone] = 1 , [EndTime] = getdate() " \
                      "WHERE ip = '%s' and dbid = %d and path = '%s'" % (ip, db_id, path)
                conn.insert_sql(sql)

        except Exception, e:
            print e
            return u"执行失败"
    else:
        print result
        print u"数据库%s在%s下的脚本已经执行成功" % (db_name, path)


# 获取用户执行计划
def get_plan_info(request):
    user_id = request.session['user_id']
    action_ip = dbregister_views.get_action_ip(request)
    conn = dbconnecter.Connection(action_ip)
    sql = "SELECT top 25 [IP],[DbID],[AccountID],[StartTime],[EndTime],[IsDone],[ID] FROM [dbo].[Exec_PlanInfo] " \
          "where [UserID] = %d order by IsDone ,StartTime desc,EndTime DESC" % user_id
    result = list(conn.select_sql(sql))

    column = ['IP', 'DbID', 'AccountID', 'StartTime', 'EndTime', 'IsDone', 'ID']
    plan_info = []
    for i in result:
        i = list(i)
        i[1] = get_database_with_id(action_ip, i[1])['DbName']
        i[2] = get_account_with_id(action_ip, i[2])['AccountName']
        i[3], i[4] = str(i[3])[:-7], str(i[4])[:-7]
        if not i[5]:
            i[5] = u"未完成"
        else:
            i[5] = u"执行成功"

        plan_info.append(dict(zip(column, i)))

    return HttpResponse(json.dumps(plan_info))
