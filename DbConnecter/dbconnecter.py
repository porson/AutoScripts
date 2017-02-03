# coding=utf-8
import pymssql


class Connection(object):
    """
    数据库连接对象，用于操作数据库
    """

    def __init__(self, action_ip, host='127.0.0.1', user='user_app_BeisenAutoScripts', password='abcdeF1',
                 database='BeisenAutoScripts'):
        """
        初始化数据库连接，默认连接本地数据库
        """
        print "Init connection..."
        try:
            self.connetion = pymssql.connect(host, user, password, database)
            self.action_ip = action_ip
        except Exception, e:
            print "Connection failed."
            print e

    def __del__(self):
        self.connetion.close()

    def account_validate(self, ip, account):
        """
        账号注册验证
        :param ip: 注册IP
        :param account: 注册账号
        :return: bool
        """
        sql = "select account from Info_DbAccount where ip = '%s' and account = '%s' " % (ip, account)
        result = self.select_sql(sql)
        if result.__len__() == 0:
            return True
        else:
            self.write_log(self.action_ip, 0, account, '')
            return False

    def database_validate(self, ip, dbname):
        """
        数据库注册验证
        :param ip: 注册IP
        :param account: 注册数据库名
        :return: bool
        """
        sql = "select dbname from Info_DatabaseInfo where ip = '%s' and dbname = '%s' " % (ip, dbname)
        result = self.select_sql(sql)
        print result
        if result.__len__() == 0:
            return True
        else:
            self.write_log(self.action_ip, 0, '', dbname)
            return False

    def create_database(self, dbip, name, info):
        """
        日志类型：1
        调用之后会关闭连接对象
        :param dbip: 数据库所在IP
        :param name: 数据库名
        :param info: 数据库备注信息
        :param action_ip: 创建人IP地址
        :return: 无
        """
        # 记录日志
        self.write_log(self.action_ip, 1, '', name)
        sql = "INSERT INTO Info_DatabaseInfo([IP],[DbName],[Info],[CreateTime],[IsActive],[DeleteTime],[EnvType]) " \
              "VALUES ('%s','%s','%s',getdate(),0,getdate(),3)" % (dbip, name, info)

        print sql
        self.insert_sql(sql)
        self.__del__()

    def create_user(self, ip, name, password, info):
        """
        日志类型：2
        调用之后会关闭连接对象
        :param ip:
        :param name:
        :param info:
        :param action_ip:
        :return:
        """
        # 记录日志
        self.write_log(self.action_ip, 2, name, '')
        # 生成SQL
        sql = "INSERT INTO " \
              "Info_DbAccount([IP],[Account],[Password],[Info],[CreateTime],[IsActive],[DeleteTime],[EnvType])" \
              " VALUES ('%s','%s','%s','%s',getdate(),0,getdate(),3)" % (ip, name, password, info)
        # 插入
        self.insert_sql(sql)
        self.__del__()

    def write_log(self, action_ip, action_type, use_account, use_db_name, env_type=3, info=''):
        print "### Writing Log .."
        sql = "INSERT INTO Info_ToolsLog(ExecIP,ActionType,UseAccount,UseDbName,ActionTime,EnvType,ErrorInfo) " \
              "VALUES ('%s','%d','%s','%s',getdate(),'%d','%s')" \
              % (action_ip, action_type, use_account, use_db_name, env_type, info)

        self.insert_sql(sql)
        print "### Log end."

    def insert_sql(self, sql):
        print sql
        try:
            cursor = self.connetion.cursor()
            cursor.execute(sql)
            self.connetion.commit()
            print "### Insert successed and closed this connection."
            cursor.close()
        except Exception, e:
            #self.write_log(self.action_ip, 9, '', '', 3, sql)
            print "### Insert failed."
            print e

    def select_sql(self, sql):
        print sql
        try:
            cursor = self.connetion.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            print "### Select successed and closed this connection."
            cursor.close()
            return result
        except Exception, e:
            print "### Select failed."
            #self.write_log(self.action_ip, 19, '', '', 3, sql)
            print e
            return []


def password_encoding(s):
    import base64
    password = base64.encodestring(s)
    return password


def password_decoding(s):
    import base64
    password = base64.decodestring(s)
    return password

