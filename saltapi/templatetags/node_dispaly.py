from saltapi import models
from django import template


register = template.Library()

@register.filter
def agent_state(status):
    try:
        if status == "None":
            res_str = '<div class="label label-table label-default">未安装</div>'
        elif status == "Active":
            res_str = '<div class="label label-table label-success">已安装</div>'
        elif status == "Deploy":
            res_str = '<div class="label label-table label-mint">安装中</div>'
        elif status == "Disabled":
            res_str = '<div class="label label-table label-dark">已下线</div>'
        elif status == "Error":
            res_str = '<div class="label label-table label-danger">安装失败</div>'
        else:
            res_str = ""
        return res_str

    except Exception as e :
        print(e)

@register.filter
def date_obj(date):

    return date.strftime('%Y-%m-%d %H:%M:%S')