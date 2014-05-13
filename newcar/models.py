#-*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


class Nation(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    ename = models.CharField(max_length=50, unique=True)

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    nation = models.ForeignKey(Nation)
    addr1 = models.CharField(max_length=30)
    addr2 = models.CharField(max_length=30)

class Maker(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    def __unicode__(self):
        return self.name

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    maker = models.ForeignKey(Maker)
    name = models.CharField(max_length=50, unique=True)
    def __unicode__(self):
        return self.name

class Trim(models.Model):
    id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Dealer(models.Model):
    user = models.OneToOneField(User)
    maker = models.ForeignKey(Maker)
    branch = models.CharField(max_length=20)    
    intro = models.TextField(null=True)       
    phone = models.CharField(max_length=12, null=False)
    addr1 = models.CharField(max_length=20)
    addr2 = models.CharField(max_length=30)
    addr3 = models.CharField(max_length=100, blank=True)
    is_confirmed = models.BooleanField(default=False)
    num_seed = models.PositiveIntegerField(default=3)        # seed(보낼 수 있는 횟수)
    num_send = models.PositiveIntegerField(default=0)        # 총 견적 송신 횟수
    num_sell = models.PositiveIntegerField(default=0)
    date_last_send = models.DateField(null=True)    # 최종 견적 송신 일자
    num_new_sell = models.PositiveIntegerField(default=0) 
    reputation = models.FloatField(default=3)                # 평판 (5점만점)
    def __unicode__(self):
        return self.user.username

class Buy(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    maker = models.ForeignKey(Maker)
    car = models.ForeignKey(Car)
    trim = models.ForeignKey(Trim)
    is_lease = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    cellphone = models.CharField(max_length=15)
    detail = models.CharField(max_length=100, null=True, help_text='Color, Option, etc.')
    addr1 = models.CharField(max_length=20)
    addr2 = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=10, blank=True)
    req_date = models.DateTimeField(auto_now_add=True, editable=False)
    is_confirmed = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)
    done_date = models.DateTimeField(null=True)   # 취소 또는 완료된 날짜
    dealer = models.ForeignKey(Dealer, null=True)    # 완료된 경우 성사된 딜러
    dealer_email = models.EmailField(max_length=50, blank=True)  # 성사된 딜러 메일
    satisfaction = models.PositiveIntegerField(default=3, validators=[MaxValueValidator(5)])
    def __unicode__(self):
        return self.user.username

# 딜러의 구매요청 조회 기록
class DealerInquiryLog(models.Model):
    id = models.AutoField(primary_key=True)
    dealer = models.ForeignKey(User, db_index=True)
    buy = models.ForeignKey(Buy)
    inquiry_date = models.DateField()
