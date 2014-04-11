#-*- coding: utf-8 -*-
from rest_framework import serializers
from newcar.models import Maker, Car, Buy

class MakerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Maker
    fields = ('mid', 'mcode', 'mname')

class CarSerializer(serializers.ModelSerializer):
  class Meta:
    model = Car
    fields = ('cid', 'mid', 'ccode', 'cname', 'trim')

# 구매요청 등록 시 사용
class BuyRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Buy
    fields = ('mid', 'cid', 'is_lease', 'is_new', 'year', 'nickname',
              'cellphone', 'email', 'passwd', 'detail', 'city', 'addr1',
              'addr2', 'req_date', 'is_done', 'is_cancel', 'done_date',
              'did', 'satisfaction')

# 무료로 조회 가능한 구매요청 목록
class BuyListFreeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Buy
    fields = ('mid', 'cid', 'is_lease', 'is_new', 'year', 'city', 'addr1', 'req_date')

# 유료로 조회 가능한 구매요청 목록
class BuyListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Buy
    fields = ('mid', 'cid', 'is_lease', 'is_new', 'year', 'nickname', 'detail', 'city',
              'addr1', 'req_date')

