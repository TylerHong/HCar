#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Form, ModelChoiceField
from django.contrib.auth.models import User
from newcar.models import Buy, Dealer, Maker, Car, Address
import pdb

class CascadeForm(forms.Form):
  maker = forms.ModelChoiceField(Maker.objects.all())
  car = forms.ModelChoiceField(Car.objects.none())
  def __init__(self, *args, **kwargs):
    forms.Form.__init__(self, *args, **kwargs)
    makers=Maker.objects.all()
    if len(makers)==1:
      self.fields['maker'].initial=makers[0].id
    maker_id=self.fields['maker'].initial or self.initial.get('maker') or self._raw_value('maker')
    if maker_id:
      cars = Car.objects.filter(maker__id=maker_id)
      self.fields['car'].queryset = cars
      if len(cars)==1:
        self.fields['car'].initial=cars[0].id

# 웹 신규등록시 주소를 두단계로 구분하기 위함
class NewBuyForm(ModelForm):
#  mid = forms.ModelChoiceField(queryset=Maker.objects.all())
#  cid = forms.ModelChoiceField(queryset=Car.objects.all())
#  passwd = forms.CharField(widget=forms.PasswordInput())
#  def __init__(self, *args, **kwargs):
#    pdb.set_trace()
#    maker_id = kwargs.pop('maker_id', None)
#    super(NewBuyForm, self).__init__(*args, **kwargs)
#    if maker_id:
#      cid = forms.ModelChoiceField(queryset=Car.objects.filter(mid=maker_id))
#  def __init__(self, *args, **kwargs):
#    pdb.set_trace()
#    maker_id = kwargs.pop('maker_id', None)
#    super(NewBuyForm, self).__init__(*args, **kwargs)
#    if maker_id:
#      cid = forms.ModelChoiceField(queryset=Car.objects.filter(mid=maker_id))
  passwd = forms.CharField(widget=forms.PasswordInput())
  addr1 = forms.ModelChoiceField(Address.objects.distinct('addr1').values_list('addr1', flat=True))
  addr2 = forms.ModelChoiceField(Address.objects.distinct('addr2').values_list('addr2', flat=True))
  class Meta:
    model = Buy
    fields = ('maker', 'car', 'trim', 'name', 'email', 'passwd',
              'cellphone', 'detail', 'zipcode')

class BuyForm(ModelForm):
  class Meta:
    model = Buy
    fields = ('maker', 'car', 'trim', 'name', 'email', 'passwd',
              'cellphone', 'detail', 'addr1', 'addr2', 'zipcode')

class ChangeBuyForm(ModelForm):
  passwd = forms.CharField(widget=forms.PasswordInput())
  class Meta:
    model = Buy
    fields = ['maker', 'car', 'trim', 'name', 'email', 'passwd',
              'cellphone', 'detail', 'addr1', 'addr2', 'zipcode', 'is_cancel']

class VerifyBuyForm(ModelForm):
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
    fields = ['maker', 'branch', 'intro', 'phone', 'addr1', 'addr2', 'addr3']

