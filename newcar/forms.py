#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from newcar.models import Buy, Dealer

class BuyForm(ModelForm):
    passwd = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Buy
        fields = ['mid', 'cid', 'tid', 'nickname', 'email', 'passwd',
                  'cellphone', 'detail', 'addr1', 'addr2', 'zipcode']

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class DealerForm(ModelForm):
    class Meta:
        model = Dealer
        fields = ['mid', 'branch_name', 'memo', 'phone', 'addr1', 'addr2', 'addr3']

