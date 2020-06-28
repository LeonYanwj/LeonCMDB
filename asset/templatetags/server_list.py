# -*- coding:UTF-8 -*-
__author__ = "Leon"
from django import template


register = template.Library()

@register.filter
def judgment_str(str_list):
    if not str_list:
        return "---"
    else:
        return str_list