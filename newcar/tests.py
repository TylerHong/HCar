#-*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from newcar.models import Maker, Car
import json
import pdb
class TestRegisterBuy(TestCase):
  def setUp(self):
    maker = Maker.objects.create(mcode="HD", mname="현대")
    Car.objects.create(mid=maker, cname="쏘나타", ccode="YF2014")
    pdb.set_trace()
  def test_1(self):
    self.c = Client()
#    json_str = u'{"mid":"1", "cid":"1", "is_lease":"False", "is_new":"True", "year":"2014", "nickname":"kshong", "cellphone":"1234", "email":"email@email.com", "passwd":"passwd", "detail":"", "city":"서울시", "addr1":"강남구", "addr2":""}'
    json_str = {"mid":1, "cid":1, "is_lease":"False", "is_new":"True", "year":"2014", "nickname":"kshong", "cellphone":"1234", "email":"email@email.com", "passwd":"passwd", "detail":"", "city":"서울시", "addr1":"강남구", "addr2":""}
#    json_string json.dumps =(json_str)
    self.response = self.c.post('/hcar/registbuy/', json.dumps(json_str), content_type='application/json')
    print(self.response)
    self.assertEqual(self.response.status_code, '201')

