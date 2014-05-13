#-*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from newcar import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/?', include(admin.site.urls)),
    url(u'^nuevo/$', views.Index.as_view()),

    # Product information request URL
    url(u'^nuevo/car/?$', views.CarList.as_view()),
    url(u'^nuevo/car/(?P<mid>[0-9]+)/?$', views.CarList.as_view()),
    url(u'^nuevo/car/(?P<mid>[0-9]+)/(?P<cid>[0-9]+)/?$', views.CarList.as_view()),
    url(u'^nuevo/car/(?P<mid>[0-9]+)/(?P<cid>[0-9]+)/(?P<tid>[0-9]+)/?$', views.CarList.as_view()),
    url(u'^nuevo/address/(?P<nid>[0-9]+)/?$', views.AddressList.as_view()),

    # consumer related  URL
    url(u'^nuevo/consumer/request/?$', views.BuyNew.as_view()), 
    url(u'^nuevo/consumer/confirm/(?P<bid>[0-9]+)/?$', views.BuyConfirm.as_view()), 
    url(u'^nuevo/consumer/query/?$', views.BuyQuery.as_view()), 
    url(u'^nuevo/consumer/modify/(?P<bid>[0-9]+)/?$', views.BuyModify.as_view()),  
    url(u'^nuevo/consumer/done/(?P<bid>[0-9]+)/?$', views.BuyDone.as_view()), 
    url(u'^nuevo/getcid/?$', views.GetCID.as_view(), name="get_cid"),    # preparing ajax

    # delaer related URL
    url(u'^nuevo/dealer/register/?$', views.DealerRegister.as_view()), 
    url(u'^nuevo/dealer/confirm/(?P<id>[0-9]+)/?$', views.DealerConfirm.as_view()), 
    url(u'^nuevo/dealer/login/?$', views.DealerLogin.as_view()),   
    url(u'^nuevo/dealer/logout/?$', views.DealerLogout.as_view()), 
    url(u'^nuevo/dealer/list/(?P<mid>[0-9]+)/?$', views.BuyListFree.as_view()), 
    url(u'^nuevo/dealer/list/(?P<mid>[0-9]+)/(?P<cid>[0-9]+)/?$', views.BuyListFree.as_view()),
    url(u'^nuevo/dealer/list/(?P<mid>[0-9]+)/(?P<cid>[0-9]+)/(?P<addr1>[0-9a-zA-Z가-힣]+)/?$',
        views.BuyListFree.as_view()),
    
)

urlpatterns = format_suffix_patterns(urlpatterns)

