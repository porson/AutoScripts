# coding:utf8
from DbConnecter import dbconnecter


def insert_login(action_ip, ldap_account):
    sql = "INSERT INTO [dbo].[Info_Users]([LdapAccount],[LastLoginIp],[LastLoginTime])" \
          "VALUES('%s','%s',GETDATE())" % (ldap_account, action_ip)
    c = dbconnecter.Connection(action_ip)
    c.insert_sql(sql)
    c.__del__()


def update_login_time(action_ip, ldap_account):
    sql = "update [dbo].[Info_Users] set [LastLoginIp] = '%s', [LastLoginTime] = getdate() where [LdapAccount] = '%s'" \
          % (action_ip, ldap_account)
    c = dbconnecter.Connection(action_ip)
    c.insert_sql(sql)
    c.__del__()


def get_ldap_id(action_ip, ldap_account):
    sql = "SELECT [id] FROM [dbo].[Info_Users] WHERE [LdapAccount] = '%s'" % ldap_account
    c = dbconnecter.Connection(action_ip)
    result = c.select_sql(sql)
    c.__del__()
    if result.__len__() == 0:
        return []
    else:
        return result[0]


def login_control(action_ip, ldap_account):
    result = get_ldap_id(action_ip, ldap_account)
    if result.__len__() == 0:
        insert_login(action_ip, ldap_account)
        ldap_id = get_ldap_id(action_ip, ldap_account)[0]
        return ldap_id
    else:
        update_login_time(action_ip, ldap_account)
        ldap_id = get_ldap_id(action_ip, ldap_account)[0]
        return ldap_id


