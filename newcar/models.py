#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Nation(models.Model):
    nid = models.PositiveIntegerField(primary_key=True)
    nname = models.CharField(max_length=50)
    nename = models.CharField(max_length=50, unique=True)

class Address(models.Model):
    aid = models.AutoField(primary_key=True)
    nid = models.ForeignKey(Nation)
    addr1 = models.CharField(max_length=30)
    addr2 = models.CharField(max_length=30)

class Maker(models.Model):
    mid = models.AutoField(primary_key=True)
    mname = models.CharField(max_length=50, unique=True)
    def __unicode__(self):
        return self.mname

class Car(models.Model):
    cid = models.AutoField(primary_key=True)
    mid = models.ForeignKey(Maker)
    cname = models.CharField(max_length=50, unique=True)
    def __unicode__(self):
        return self.cname

class Trim(models.Model):
    tid = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Car)
    tname = models.CharField(max_length=50)
    def __unicode__(self):
        return self.tname

class Dealer(models.Model):
    user = models.OneToOneField(User)
    mid = models.ForeignKey(Maker)
    branch = models.CharField(max_length=20)    # 지점명
    intro = models.TextField(null=True)         # 자기소개
    phone = models.CharField(max_length=12, null=True)
    addr1 = models.CharField(max_length=20)
    addr2 = models.CharField(max_length=30)
    addr3 = models.CharField(max_length=100, blank=True)
    is_confirmed = models.BooleanField(default=False)
    num_seed = models.PositiveIntegerField(default=3)        # seed(견적 보낼 수 있는 횟수)
    num_send = models.PositiveIntegerField(default=0)        # 총 견적 송신 횟수
    date_last_send = models.DateField(null=True)    # 최종 견적 송신 일자
    num_new_sell = models.PositiveIntegerField(default=0)    # 신차 판매 대수
    reputation = models.FloatField(default=3)                # 평판 (5점만점)
    def __unicode__(self):
        return self.user.username

class Buy(models.Model):
    bid = models.AutoField(primary_key=True)
    mid = models.ForeignKey(Maker)
    cid = models.ForeignKey(Car)
    tid = models.ForeignKey(Trim)
    is_lease = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, null=False)
    passwd = models.CharField(max_length=25)
    cellphone = models.CharField(max_length=15)
    detail = models.CharField(max_length=100, null=True)
    addr1 = models.CharField(max_length=20)
    addr2 = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=10, null=True)
    req_date = models.DateTimeField(auto_now_add=True, editable=False)
    is_confirmed = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)
    done_date = models.DateTimeField(null=True)   # 취소 또는 완료된 날짜
    did = models.ForeignKey(Dealer, null=True)    # 완료된 경우 성사된 딜러
    satisfaction = models.PositiveIntegerField(default=3)
    def __unicode__(self):
        return str(self.bid)+' '+str(self.mid)+' '+str(self.cid)+' '+self.nickname

# 딜러의 구매요청 조회 기록
class DealerInquiryLog(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(User, db_index=True)
    bid = models.ForeignKey(Buy)
    inquiry_date = models.DateField()
