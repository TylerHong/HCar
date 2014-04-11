#-*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from newcar.models import Maker, Car, Buy
import json
import pdb

class TestBuyListFree(TestCase):
  def setUp(self):
    makerHD = Maker.objects.create(mcode="HD", mname="현대")
    makerKA = Maker.objects.create(mcode="KA", mname="기아")
    carLF = Car.objects.create(mid=makerHD, cname="쏘나타LF", ccode="YF2014")
    carK5 = Car.objects.create(mid=makerKA, cname="K5", ccode="K52014")
    carHG = Car.objects.create(mid=makerHD, cname="그랜저HG", ccode="HG2014")
    Buy.objects.create(mid=makerHD, cid=carLF, year=2014, nickname='홍길동', cellphone='01012345678',
      email='email@email.com', passwd='1234', city='서울시', addr1='강남구')
    Buy.objects.create(mid=makerKA, cid=carK5, year=2014, nickname='김태희', cellphone='01012345678',
      email='1mail@email.com', passwd='1234', city='울산시', addr1='강남구')
    Buy.objects.create(mid=makerHD, cid=carHG, year=2014, nickname='정우성', cellphone='01012345678',
      email='2mail@email.com', passwd='1234', city='서울시', addr1='강남구')
    Buy.objects.create(mid=makerKA, cid=carK5, year=2014, nickname='수지', cellphone='01012345678',
      email='3mail@email.com', passwd='1234', city='성남시', addr1='분당구')
    self.c = Client()

  def test_newcar(self):
#  def test_register_request_fail(self):
    json_str = {"mid":1, "cid":1, "is_lease":"False", "is_new":"True", "year":"2014", "nickname":"kshong",
      "cellphone":"1234", "email":"email@email.com", "passwd":"passwd", "detail":"", "city":"서울시",
      "addr1":"강남구", "addr2":""}
    self.response = self.c.post('/hcar/buyrequest/', json.dumps(json_str), content_type='application/json')
    pdb.set_trace()
    print(self.response)
    self.assertEqual(self.response.status_code, 409)

#  def test_register_request_success(self):
    json_str = {"mid":1, "cid":1, "is_lease":"False", "is_new":"True", "year":"2014", "nickname":"kshong",
      "cellphone":"1234", "email":"tctgkiss@hanmail.net", "passwd":"passwd", "detail":"", "city":"서울시",
      "addr1":"강남구", "addr2":""}
    self.response = self.c.post('/hcar/buyrequest/', json.dumps(json_str), content_type='application/json')
    pdb.set_trace()
    print(self.response)
    self.assertEqual(self.response.status_code, 201)

#  def test_search_free(self):
#    json_str = {"mid":5, "city":"ANY"}
#    self.response = self.c.post('/hcar/buylist/', json.dumps(json_str), content_type='application/json')
    self.response = self.c.get('/hcar/buylist/1/0/ANY/', content_type='application/json')
    pdb.set_trace()
    print(self.response)
    self.assertEqual(self.response.status_code, 200)

    self.response = self.c.get('/hcar/buylist/2/2/ANY/', content_type='application/json')
    pdb.set_trace()
    print(self.response)
    self.assertEqual(self.response.status_code, 200)
