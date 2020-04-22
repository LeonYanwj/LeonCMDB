#-*-conding:utf-8-*-
__author__ = 'Leonyan'


from django.conf.urls import url,include
from salt_restapi import views


urlpatterns = [
    url(r'^batch_add/',views.batch_add,name="batch_add"),
]
