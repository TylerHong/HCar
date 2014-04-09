#-*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from newcar import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/?', include(admin.site.urls)),

    # 이하 자동차 목록 요청 URL
    url(u'^hcar/carlist/?$', views.CarList.as_view()),
    url(u'^hcar/carlist/(?P<mcode>[a-zA-Z]+)/?$', views.CarList.as_view()),
    url(u'^hcar/carlist/(?P<mcode>[a-zA-Z]+)/(?P<ccode>[a-zA-Z0-9]+)/?$', views.CarList.as_view()),

    # 이하 구매등록 URL
    url(u'^hcar/registbuy/?$', views.RegisterBuy.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)

