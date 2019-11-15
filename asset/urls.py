#_*_conding:utf-8_*_
__author__ = 'Leonyan'


from django.conf.urls import url
from asset import views

urlpatterns = [
    url(r'report/asset_with_no_asset_id/$', views.asset_with_no_asset_id),
    url(r'report/$', views.asset_report),
]
