# coding=utf-8
import os
import re


# SQL内容校验
import chardet


def check_sql_content(f):
    # 获取文件编码
    code_style = chardet.detect(f.read()).get('encoding')
    print code_style

    # 重置文件对象指针
    f.seek(0, os.SEEK_SET)

    # 针对Unicode做特殊处理
    if code_style == "UTF-16LE":
        sql_content = f.read().decode('utf-16', 'ignore')
    else:
        sql_content = f.read().decode(code_style)

    # 将读取内容切片
    sql_content = sql_content.split('\r\n')
    print sql_content

    # 返回结果集初始化
    error_info = []  # 错误信息

    # 脚本内容检测正则匹配规则
    p_update = '^update\s+.*'
    p_use = '^use\s+.*'
    p_procedure = '^procedure\s+.*'
    p_create = '^create\s+.*'
    p_delete = '^delete\s+.*'

    # 匹配内容计数器
    c_database = 0
    c_use = 0
    c_procedure = 0
    c_create = 0
    c_delete = 0
    c_update = 0

    database = ''

    # 获取脚本内的数据库名称
    for line in sql_content:
        print line.encode('utf8')
        if re.match(p_use, line.lstrip(), re.IGNORECASE):
            c_use += 1
            database = re.sub('use ', '', line.lower().strip()).replace('[', '').replace(']', '')
            print database
            c_database += 1

    # 根据获取的数据库生成数据库名匹配规则
    p_database = '.* %s.*' % database

    # 根据正则表达式对文本内容进行统计
    for line in sql_content:
        if re.match(p_database, line, re.IGNORECASE):
            c_database += 1

        if re.match(p_procedure, line.lstrip(), re.IGNORECASE):
            c_procedure += 1

        if re.match(p_create, line.lstrip(), re.IGNORECASE):
            c_create += 1

        if re.match(p_delete, line.lstrip(), re.IGNORECASE):
            c_delete += 1

        if re.match(p_update, line.lstrip(), re.IGNORECASE):
            c_update += 1

    print database
    print c_database

    # 整合错误信息
    # if database != exec_db:
    #     error_info.append(u'数据库%s与选择的数据库%s不匹配' % (database, exec_db))

    if c_use == 0:
        error_info.append(u'未指定执行的数据库')

    if c_procedure > 2:
        error_info.append(u'脚本中包含多个存储过程')

    if c_database > 3:
        error_info.append(u'数据库名出现多次，请确认未写死数据库名')

    if c_use > 1:
        error_info.append(u'多次USE数据库')

    if c_update > 1:
        error_info.append(u'一个脚本内含有多个UPDATE语句，无法保证数据安全')

    # 根据错误信息返回校验结果
    if error_info.__len__() == 0:
        check_result = True
    else:
        check_result = False

    return {'result': check_result, 'error': error_info}
