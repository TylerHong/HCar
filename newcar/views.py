#-*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from newcar.models import Maker, Car, Buy
from newcar.serializers import MakerSerializer, CarSerializer, BuyRegisterSerializer

import pdb;

# 제조사 및 자동차 리스트를 가져오는 REST 뷰
class CarList(APIView):
    def get(self, request, mcode='aa', ccode='ANY', format=None):
        # 아무 조건도 없다면 메이커 명을 리턴
        if (mcode == 'aa'):
            makers = Maker.objects.all().order_by('mid')
            if request.accepted_renderer.format == 'html':
                data = {'makers': makers}
                return Response(data, template_name='makerlist.html')
            else:
                serializer = MakerSerializer(makers, many=True)
                return Response(serializer.data)
        # 메이커명이 주어졌다면 자동차명을 리턴
        elif (mcode <> 'aa' and ccode == 'ANY'):
            maker = Maker.objects.filter(mcode=mcode).order_by('mid')
            cars = Car.objects.filter(mid=maker).order_by('cid')
            if request.accepted_renderer.format == 'html':
                data = {'cars': cars}
                return Response(data, template_name='carlist.html')
            else:
                serializer = CarSerializer(cars, many=True)
                return Response(serializer.data)
        # 메이커명과 자동차명이 주어졌다면 사양을 리턴
        elif (mcode <> 'aa' and ccode <> 'ANY'):
            maker = Maker.objects.filter(mcode=mcode).order_by('mid')
            cars = Car.objects.filter(mid=maker, ccode=ccode).order_by('cid')
            if request.accepted_renderer.format == 'html':
                data = {'cars': cars}
                return Response(data, template_name='carlist.html')
            else:
                serializer = CarSerializer(cars, many=True)
                return Response(serializer.data)

# 구매요청 등록 뷰
class RegisterBuy(APIView):
    def post(self, request, format=None):
        pdb.set_trace()
        serializer = BuyRegisterSerializer(data=request.DATA)
        if serializer.is_valid():
            # 동일 전화번호/이메일로 구매 요청이 있는지 확인
            try:
                oldReq = Buy.objects.get(email=serializer.data['email'], is_done=False)
            except Buy.DoesNotExist:
                try:
                    oldReq = Buy.objects.get(email=serializer.data['email'])
                except Buy.DoesNotExist:
                    serializer.save()
                    data = {'msg':'saved', 'errcode':'000'}
                    return Response(data, status = status.HTTP_201_CREATED)
                else:
                    data = {'msg':'save failed. same email exists', 'errcode':'101'}
            else:
                data = {'msg':'save failed. same phone exists', 'errcode':'101'}
                return Response(data, status = status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            data = {'msg':'invalid request', 'errcode':'102'}
            return Response(data, status = status.HTTP_503_SERVICE_UNAVAILABLE)

# 구매요청 검색 뷰
class FindBuy(APIView):
    def get(self, request, mid, cid, is_lease, city='ANY', addr1='ANY', addr2='ANY', req_date=0, format=None):
        if (mid <= 0 or cid <=0):
            response.status_code = status.HTTP_400_BAD_REQUEST
        return response

