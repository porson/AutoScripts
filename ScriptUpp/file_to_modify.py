# coding:utf8
# 文件转unicode
import re

import chardet
import os


# 文件落盘
def save_file_to_disk(f, fp):
    # 重置文件对象指针
    f.seek(0, os.SEEK_SET)
    try:
        new_file = open(fp, 'wb+')
        new_file.write(f.read())
        new_file.close()
        return True
    except Exception, e:
        print e
        return False


#
def change_file_to_utf8(fp):
    files = os.listdir(fp)
    for f in files:
        path = os.path.join(fp, f)
        f_reader = open(path, 'rb')
        # 获取文件编码
        code_style = chardet.detect(f_reader.read()).get('encoding')
        # 重置文件对象指针
        f_reader.seek(0, os.SEEK_SET)
        content_change = []
        # 获取内容开始转码
        try:
            if code_style == 'UTF-16LE':
                content_change = f_reader.read().decode('utf16', 'ignore').encode('utf8')
            else:
                content_change = f_reader.read().decode(code_style).encode('utf8')
        except Exception, e:
            print u"转码失败"
            print u"编码为%s" % code_style
            print str(e)

        with open(path, 'w') as newFile:
            newFile.writelines(content_change)
            newFile.close()


# 去掉USE
def remove_use(fp):
    files = os.listdir(fp)
    pattern = r'^use\s+.*'
    for f in files:
        path = os.path.join(fp, f)
        fr = open(path, 'rb')
        content = fr.readlines()
        for i in content:
            if re.match(pattern, i.lstrip(), re.IGNORECASE):
                print i
                content.remove(i)
        fr.close()
        with open(path, 'w') as newFile:
            newFile.writelines(content)
            newFile.close()
