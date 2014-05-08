#-*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from newcar.models import Maker, Car, Trim, Buy, Dealer, Address

class MakerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Maker
    fields = ('id', 'name')

class CarSerializer(serializers.ModelSerializer):
  class Meta:
    model = Car
    fields = ('id', 'maker', 'name')

class TrimSerializer(serializers.ModelSerializer):
  class Meta:
    model = Trim
    fields = ('id', 'car', 'name')

class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Address
    fields = ('addr1', 'addr2')

# 구매요청 등록 시 사용
class BuyRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Buy
    fields = ('maker', 'car', 'trim', 'is_lease', 'is_new', 'name',
              'email', 'passwd', 'cellphone', 'detail', 'addr1', 'addr2', 'zipcode')

class VerifyBuySerializer(serializers.ModelSerializer):
  class Meta:
    model = Buy
    fields = ('email', 'passwd')

class ChangeBuySerializer(serializers.ModelSerializer):
  class Meta:
    model = Buy
    fields = ('maker', 'car', 'trim', 'is_lease', 'is_new', 'name',
              'email', 'passwd', 'cellphone', 'detail', 'addr1', 'addr2', 'zipcode', 'is_cancel')

# 무료로 조회 가능한 구매요청 목록
class BuyListFreeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Buy
    fields = ('maker', 'car', 'trim', 'is_lease', 'is_new', 'addr1', 'addr2', 'req_date')

# 유료로 조회 가능한 구매요청 목록
class BuyListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Buy
    fields = ('maker', 'car', 'trim', 'is_lease', 'is_new', 'name', 'detail', 'addr1',
              'addr2', 'req_date')

class LoginSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'password')

class NewUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'email', 'password')

class NewDealerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Dealer
    fields = ('user', 'maker', 'branch', 'intro', 'phone', 'addr1', 'addr2', 'addr3')

