#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from newcar.models import Buy, Dealer

class NewBuyForm(ModelForm):
    passwd = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Buy
        fields = ['mid', 'cid', 'tid', 'nickname', 'email', 'passwd',
                  'cellphone', 'detail', 'addr1', 'addr2', 'zipcode']

class ChangeBuyForm(ModelForm):
    passwd = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Buy
        fields = ['email', 'passwd']

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class DealerForm(ModelForm):
    class Meta:
        model = Dealer
        fields = ['mid', 'branch', 'intro', 'phone', 'addr1', 'addr2', 'addr3']

