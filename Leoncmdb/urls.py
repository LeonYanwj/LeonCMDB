"""Leoncmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from asset import urls as asset_urls
from Leoncmdb import urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^asset/',include(asset_urls)),
    url(r'^search/',include('Lesearch.urls')),
    url(r'^login.html/$',asset_urls.views.login),
    url(r'^logout/$',asset_urls.views.logout),
    url(r'^index.html/$',asset_urls.views.index),
    url(r'^$',asset_urls.views.root),
]
