# coding=utf-8
from django.conf.urls import url

from DbRegister import views as register_view
from DbRegister import show_info as register_show
from ScriptUpp import views as script_upp_view
from ScriptUpp import sqlplan
from SystemLogs import view as log_view
from LdapCheck import view as login_view

urlpatterns = [
    url(r'^$', login_view.index),
    url(r'^login/$', login_view.login),
    url(r'^welcome/$', script_upp_view.index),

    url(r'^register/$', register_view.index),
    url(r'^register_register/$', register_view.register),
    url(r'^register_show_database/$', register_show.get_databases),
    url(r'^register_show_account/$', register_show.get_accounts),

    url(r'^logs/$', log_view.index),
    url(r'^logs/(.+)/$', log_view.get_log),

    # 前端交互接口
    url(r'^get_ip_from_db/$', register_show.get_ip_from_db),
    url(r'^get_db_with_ip/(.+)/$', register_show.get_databases_with_ip),
    url(r'^get_account_with_ip/(.+)/$', register_show.get_account_with_ip),
    url(r'^get_exec_plan/$', sqlplan.get_plan_info),
    url(r'^scripts_up/$', script_upp_view.exec_sql)

]

