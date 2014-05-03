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
    url(u'^hcar/carlist/(?P<mid>[0-9]+)/?$', views.CarList.as_view()),
    url(u'^hcar/carlist/(?P<mid>[0-9]+)/(?P<cnid>[0-9]+)/?$', views.CarList.as_view()),
    url(u'^hcar/carlist/(?P<mid>[0-9]+)/(?P<cnid>[0-9]+)/(?P<cid>[0-9]+)/?$', views.CarList.as_view()),

    # 이하 구매등록 URL
    url(u'^hcar/buyrequest/?$', views.BuyRequest.as_view()),
    url(u'^hcar/confirm_buy/(?P<bid>[0-9]+)/?$', views.ConfirmBuy.as_view()),


    # 딜러 회원가입 뷰
    url(u'^hcar/register/?$', views.Register.as_view()),
    url(u'^hcar/confirm_dealer/(?P<id>[0-9]+)/?$', views.ConfirmDealer.as_view()),

    # 딜러 로그인 뷰
    url(u'^hcar/login/?$', views.Login.as_view()),
    url(u'^hcar/logout/?$', views.Logout.as_view()),

    # 구매 요청 리스트 URL for anyone
    url(u'^hcar/buylist/(?P<mid>[0-9]+)/?$', views.BuyListFree.as_view()),
    url(u'^hcar/buylist/(?P<mid>[0-9]+)/(?P<cnid>[0-9]+)/?$', views.BuyListFree.as_view()),
    url(u'^hcar/buylist/(?P<mid>[0-9]+)/(?P<cnid>[0-9]+)/(?P<city>[a-zA-Z가-힣]+)/?$', views.BuyListFree.as_view()),
    
)

urlpatterns = format_suffix_patterns(urlpatterns)

