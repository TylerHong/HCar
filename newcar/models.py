#-*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

class Nation(models.Model):
    nid = models.AutoField(primary_key=True)
    nname = models.CharField(max_length=50)
    nename = models.CharField(max_length=50)

class Maker(models.Model):
    mid = models.AutoField(primary_key=True)
    mname = models.CharField(max_length=50)
    def __unicode__(self):
        return self.mname

class CarName(models.Model):
    cnid = models.AutoField(primary_key=True)
    mid = models.ForeignKey(Maker)
    cname = models.CharField(max_length=50)
    def __unicode__(self):
        return self.cname

class CarSpec(models.Model):
    cid = models.AutoField(primary_key=True)
    cnid = models.ForeignKey(CarName)
    trim = models.Charfield(max_length=50, null=True)
    def __unicode__(self):
        return self.trim

class Dealer(models.Model):
    did = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=50)
    dname = models.CharField(max_length=20)
    passwd = models.CharField(max_length=25)
    mid = models.ForeignKey(Maker)
    branch_name = models.CharField(max_length=20)
    grade = models.CharField(max_length=1)
    memo = models.TextField(null=True)
    phone = models.CharField(max_length=12, null=True)
    city = models.CharField(max_length=20)
    addr1 = models.CharField(max_length=30)
    addr2 = models.CharField(max_length=30, null=True)
    join_date = models.DateField(auto_now_add=True, editable=False)
    is_confirmed = models.BooleanField(default=False)
    num_send = models.PositiveIntegerField(default=0)
    date_last_send = models.DateField(auto_now_add=False)
    withdraw = models.BooleanField(default=False)
    num_new_sell = models.PositiveIntegerField(default=0)
    reputation = models.FloatField(default=3)
    def __unicode__(self):
        return self.dname

class Buy(models.Model):
    bid = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Car)
    is_lease = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    year = models.PositiveIntegerField(default=0)
    nickname = models.CharField(max_length=20)
    cellphone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, null=False)
    passwd = models.CharField(max_length=25)
    detail = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=20)
    addr1 = models.CharField(max_length=30)
    addr2 = models.CharField(max_length=100, blank=True)
    req_date = models.DateTimeField(auto_now_add=True, editable=False)
    is_confirmed = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)
    done_date = models.DateTimeField(null=True)   # 취소 또는 완료된 날짜
    did = models.ForeignKey(Dealer, null=True)    # 완료된 경우 성사된 딜러
    satisfaction = models.PositiveIntegerField(default=3)
    def __unicode__(self):
        return str(self.bid)+' '+str(self.mid)+' '+str(self.cid)+' '+self.nickname

class BuyForm(ModelForm):
    class Meta:
        model = Buy
        fields = ['mid', 'cid', 'is_lease', 'is_new', 'year', 'nickname', 'cellphone', 'email',
            'passwd', 'detail', 'city', 'addr1', 'addr2']

