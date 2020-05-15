#-*-conding:utf-8-*-
__author__ = 'Leonyan'


from django.conf.urls import url,include
from saltapi import views


urlpatterns = [
    url(r'^batch_add/',views.batch_add,name="batch_add"),
    url(r'^salt_agent_deploy/',views.salt_agent_deploy,name="salt_agent_deploy"),
    url(r'^node_list.html$',views.node_list),
]
