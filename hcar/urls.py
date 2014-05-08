#-*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from newcar import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/?', include(admin.site.urls)),
    url(u'^nuevo/$', views.Index.as_view()),

    # 이하 자동차 목록 요청 URL
    url(u'^nuevo/carlist/?$', views.CarList.as_view()),
    url(u'^nuevo/carlist/(?P<mid>[0-9]+)/?$', views.CarList.as_view()),
    url(u'^nuevo/carlist/(?P<mid>[0-9]+)/(?P<cid>[0-9]+)/?$', views.CarList.as_view()),
    url(u'^nuevo/carlist/(?P<mid>[0-9]+)/(?P<cid>[0-9]+)/(?P<tid>[0-9]+)/?$', views.CarList.as_view()),

    # 이하 주소 요청 URL
    url(u'^nuevo/address/(?P<nid>[0-9]+)/?$', views.AddressList.as_view()),

    # 이하 구매등록 관련 URL
    url(u'^nuevo/buyrequest/?$', views.BuyRequest.as_view()),
    url(u'^nuevo/confirm_buy/(?P<bid>[0-9]+)/?$', views.ConfirmBuy.as_view()),
    url(u'^nuevo/buychange/?$', views.BuyChange.as_view()),


    # 딜러 회원가입 뷰
    url(u'^nuevo/register/?$', views.Register.as_view()),
    url(u'^nuevo/confirm_dealer/(?P<id>[0-9]+)/?$', views.ConfirmDealer.as_view()),

    # 딜러 로그인 뷰
    url(u'^nuevo/login/?$', views.Login.as_view()),
    url(u'^nuevo/logout/?$', views.Logout.as_view()),

    # 구매 요청 리스트 URL for anyone
    url(u'^nuevo/buylist/(?P<mid>[0-9]+)/?$', views.BuyListFree.as_view()),
    url(u'^nuevo/buylist/(?P<mid>[0-9]+)/(?P<cid>[0-9]+)/?$', views.BuyListFree.as_view()),
    url(u'^nuevo/buylist/(?P<mid>[0-9]+)/(?P<cid>[0-9]+)/(?P<addr1>[0-9a-zA-Z가-힣]+)/?$', views.BuyListFree.as_view()),
    
)

urlpatterns = format_suffix_patterns(urlpatterns)

