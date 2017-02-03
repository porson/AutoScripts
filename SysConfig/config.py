# coding:utf8
# 配置文件获取模块

import ConfigParser
import os


class Configer(object):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    CONFIG_DIR = os.path.join(BASE_DIR, "Config")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "config.conf")

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(self.CONFIG_FILE, 'rb'))

    def get_script_path(self):
        path = self.config.get('script', 'path')
        return path

    def get_expire_days(self):
        expire = self.config.get('script', 'expire')
        return expire

    def get_shell_path(self):
        shell_path = self.config.get('shell', 'path')
        return shell_path

    def get_log_path(self):
        log_path = self.config.get('script', 'log_path')
        return log_path
