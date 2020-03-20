#-*-conding:utf-8-*-
__author__ = 'Leonyan'


from django.conf.urls import url
from asset import views

urlpatterns = [
    url(r'report/asset_with_no_asset_id/$', views.asset_with_no_asset_id),
]
