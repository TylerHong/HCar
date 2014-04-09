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

class BuyRegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = Buy
    fields = ('mid', 'cid', 'is_lease', 'is_new', 'year', 'nickname',
              'cellphone', 'email', 'passwd', 'detail', 'city', 'addr1',
              'addr2', 'req_date', 'is_done', 'is_cancel', 'done_date',
              'did', 'satisfaction')

