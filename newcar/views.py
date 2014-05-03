#-*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse

from newcar.models import Maker, CarName, Car, Buy, BuyForm, Dealer, DealerForm
from newcar.serializers import MakerSerializer, CarSerializer, BuyRequestSerializer, BuyListFreeSerializer
import pdb;


# 제조사 및 자동차 리스트를 가져오는 REST 뷰
class CarList(APIView):
    def get(self, request, mid='0', cnid='0', cid='0', format=None):
        # 아무 조건도 없다면 메이커 명을 리턴
        if (mid == '0'):
            makers = Maker.objects.all().order_by('mid')
            if request.accepted_renderer.format == 'html':
                data = {'makers': makers}
                return Response(data, template_name='list_maker.html')
            else:
                serializer = MakerSerializer(makers, many=True)
                return Response(serializer.data)
        # 메이커명이 주어졌다면 자동차명을 리턴
        elif (mid <> '0' and cnid == '0'):
            maker = Maker.objects.filter(mid=mid)
            car_names = CarName.objects.filter(mid=maker).order_by('cnid')
            if request.accepted_renderer.format == 'html':
                data = {'car_names': car_names}
                return Response(data, template_name='list_carname.html')
            else:
                serializer = CarNameSerializer(car_names, many=True)
                return Response(serializer.data)
        # 메이커명과 자동차명이 주어졌다면 사양을 리턴
        elif (mid <> '0' and cnid <> '0' and cid == '0'):
            maker = Maker.objects.filter(mid=mid).order_by('mid')
            car_name = CarName.objects.filter(mid=maker, cnid=cnid)
            cars = Car.objects.filter(cnid=car_name).order_by('cid')
            if request.accepted_renderer.format == 'html':
                data = {'cars': cars}
                return Response(data, template_name='list_car.html')
            else:
                serializer = CarSerializer(cars, many=True)
                return Response(serializer.data)

# 구매요청 등록 뷰
class BuyRequest(APIView):
    def send_email(self, bid, to):
        subject = 'Confirm message from hcar'
        text_content = 'This is important message.'
        html_content = render_to_string('html_buy_confirm.html', {'id': bid})
#        msg = EmailMultiAlternatives(subject, text_content, 'kisoohong@gmail.com' , [to])
#        msg.attach_alternative(html_content, "text/html")
#        pdb.set_trace()
#        msg.send()
        send_mail(subject, html_content, 'kshong@coche.dnip.net', [to])

    def post(self, request, format=None):
        pdb.set_trace()
        # html 접근일 경우
        if request.accepted_renderer.format == 'html':
            form = BuyForm(request.POST)
            # form 확인
            if not form.is_valid():
                data = {'msg':'invalid form', 'errcode':'103'}
                respStatus = status.HTTP_400_BAD_REQUEST
                return Response(data, status = respStatus, template_name='buyrequest_result.html')
            # 동일 이메일로 완료되지 않은 구매 요청이 있는지 확인
            oldReqs = Buy.objects.filter(email=form.cleaned_data['email']).filter(is_done=False)
            if (oldReqs.count() > 0):
                data = {'msg':'save failed. same email exists', 'errcode':'101'}
                respStatus = status.HTTP_409_CONFLICT
                return Response(data, status = respStatus, template_name='buyrequest_result.html')
            # 저장후 구매 요청 확인 메일 송신
            buy = form.save()
            self.send_email(buy.bid, buy.email)
            data = {'msg':'saved', 'errcode':'000'}
            respStatus = status.HTTP_201_CREATED
            return Response(data, status = respStatus, template_name='buyrequest_result.html')
        # html 이외 접근일경우 (모바일)
        else:
            serializer = BuyRequestSerializer(data=request.DATA)
            if not serializer.is_valid():
                data = {'msg':'invalid request', 'errcode':'102'}
                respStatus = status.HTTP_400_BAD_REQUEST
                return Response(data, status = respStatus)
            # 동일 이메일로 완료되지 않은 구매 요청이 있는지 확인
            oldReqs = Buy.objects.filter(email=serializer.data['email']).filter(is_done=False)
            if (oldReqs.count() > 0):
                data = {'msg':'save failed. same email exists', 'errcode':'101'}
                respStatus = status.HTTP_409_CONFLICT
                return Response(data, status = respStatus)
            # 저장후 구매 요청 확인 메일 송신
            serializer.save()
            buy = Buy.objects.filter(email=serializer.data['email']).filter(is_done=False)
            self.send_email(buy[0].bid, buy[0].email)
            data = {'msg':'saved', 'errcode':'000'}
            respStatus = status.HTTP_201_CREATED
            return Response(data, status = respStatus)

    def get(self, request, format=None):
        if request.accepted_renderer.format == 'html':
            form = BuyForm()
            data = {'form': form}
            return Response(data, template_name='buyrequest_post.html')
        else:
            data = "GET not allowed"
            respStatus = status.HTTP_400_BAD_REQUEST
            return Response(data, status = respStatus)


# 구매요청 검증 뷰
class ConfirmBuy(APIView):
    def get(self, request, bid, format=None):
        respStatus = status.HTTP_200_OK
        if (int(bid) <= 0):
            data = {'msg':'CONFIRM ERROR'}
        else:
            try:
                buy = Buy.objects.get(bid=bid)
                if (buy.is_confirmed == True):
                    data = {'msg':'ALREADY CONFIRMED'}
                else:
                    buy.is_confirmed = True
                    buy.save()
                    data = {'msg':'CONFIRMED'}
            except Buy.DoesNotExist:
                respStatus = status.HTTP_400_BAD_REQUEST
                data = {'msg':'BAD REQUEST'}
        return Response(data, status = respStatus, template_name='confirm.html')


# 구매요청 검색 뷰 for anyone
class BuyListFree(APIView):
    def get(self, request, mid, cid, city='ANY', format=None):
#        pdb.set_trace()

        mid = int(mid)
        cid = int(cid)
        if (mid <= 0):
            data = {'msg':'invalid mid', 'errcode':'202'}
            return Response(data, status = status.HTTP_400_BAD_REQUEST)
        elif (cid < 0):
            data = {'msg':'invalid cid', 'errcode':'203'}
            return Response(data, status = status.HTTP_400_BAD_REQUEST)

        if (cid == 0):
            buyreqs = Buy.objects.filter(mid=mid).filter(is_confirmed=True)
        else:
            buyreqs = Buy.objects.filter(mid=mid).filter(cid=cid).filter(is_confirmed=True)
        if (buyreqs.count() > 0 and city <> 'ANY'):
            buyreqs = buyreqs.filter(city__contains=city)

        if (buyreqs.count() == 0):
            data = {'msg':'no data', 'errcode':'201'}
            return Response(data, status = status.HTTP_400_BAD_REQUEST)
        elif (buyreqs.count() == 1):
            serializer = BuyListFreeSerializer(buyreqs)
            return Response(serializer.data)
        else:
            serializer = BuyListFreeSerializer(buyreqs, many=True)
            return Response(serializer.data)


# 딜러 회원가입 뷰
class Register(APIView):
    def send_email(self, did, to):
        subject = 'Confirm message from hcar'
        text_content = 'This is important message.'
        html_content = render_to_string('html_dealer_confirm.html', {'id': did})
        send_mail(subject, html_content, 'kshong@coche.dnip.net', [to])

    def get(self, request, format=None):
        if request.accepted_renderer.format == 'html':
            form = DealerForm()
            data = {'form': form}
            return Response(data, template_name='register_post.html')
        else:
            data = "GET not allowed"
            respStatus = status.HTTP_400_BAD_REQUEST
            return Response(data, status = respStatus)

    def post(self, request, format=None):
        pdb.set_trace()
        # html 접근일 경우
        if request.accepted_renderer.format == 'html':
            form = DealerForm(request.POST)
            # form 확인
            if not form.is_valid():
                data = {'msg':'invalid form', 'errcode':'103'}
                respStatus = status.HTTP_400_BAD_REQUEST
                return Response(data, status = respStatus, template_name='register_result.html')
            # 동일 이메일로 등록된 딜러가 있는지 확인
            oldDealers = Dealer.objects.filter(email=form.cleaned_data['email'])
            if (oldDealers.count() > 0):
                data = {'msg':'register failed. same email exists', 'errcode':'101'}
                respStatus = status.HTTP_409_CONFLICT
                return Response(data, status = respStatus, template_name='register_result.html')
            # 저장후 딜러 확인 메일 송신
            dealer = form.save()
            self.send_email(dealer.did, dealer.email)
            data = {'msg':'saved', 'errcode':'000'}
            respStatus = status.HTTP_201_CREATED
            return Response(data, status = respStatus, template_name='register_result.html')
        # html 이외 접근일경우 (모바일)
        else:
            serializer = RegisterSerializer(data=request.DATA)
            if not serializer.is_valid():
                data = {'msg':'invalid request', 'errcode':'102'}
                respStatus = status.HTTP_400_BAD_REQUEST
                return Response(data, status = respStatus)
            # 동일 이메일로 등록된 딜러가 있는지 확인
            oldDealers = Dealer.objects.filter(email=serializer.data['email'])
            if (oldDealers.count() > 0):
                data = {'msg':'register failed. same email exists', 'errcode':'101'}
                respStatus = status.HTTP_409_CONFLICT
                return Response(data, status = respStatus)
            # 저장후 딜러 확인 메일 송신
            serializer.save()
            dealer = Dealer.objects.filter(email=serializer.data['email'])
            self.send_email(dealer[0].did, dealer[0].email)
            data = {'msg':'saved', 'errcode':'000'}
            respStatus = status.HTTP_201_CREATED
            return Response(data, status = respStatus)

# 딜러 검증 뷰
class ConfirmDealer(APIView):
    def get(self, request, did, format=None):
        respStatus = status.HTTP_200_OK
        if (int(did) <= 0):
            data = {'msg':'CONFIRM ERROR'}
        else:
            try:
                dealer = Dealer.objects.get(did=did)
                if (dealer.is_confirmed == True):
                    data = {'msg':'ALREADY CONFIRMED'}
                else:
                    dealer.is_confirmed = True
                    dealer.save()
                    data = {'msg':'CONFIRMED'}
            except Dealer.DoesNotExist:
                respStatus = status.HTTP_400_BAD_REQUEST
                data = {'msg':'BAD REQUEST'}
        return Response(data, status = respStatus, template_name='confirm.html')

# 딜러 로그인 뷰
class Login(APIView):
    def get(self, request, format=None):
        if request.accepted_renderer.format == 'html':
            request.session['coche_login_sess'] = 'hannal'
            return HttpResponse('[%s] logged in successfully' % request.session['coche_login_sess'])
        else:
            return Response(status=status.HTTP_200_OK)

# 딜러 로그아웃 뷰
class Logout(APIView):
    def get(self, request, format=None):
        if request.accepted_renderer.format == 'html':
            del request.session['coche_login_sess']
            return HttpResponse('logged out successfully')
        else:
            return Response(status=status.HTTP_200_OK)


class Logintest(APIView):
    def get(self, request, format=None):
        if request.accepted_renderer.format == 'html':
            return HttpResponse('[%s] logged in successfully' % request.session['coche_login_sess'])
        else:
            return Response(status=status.HTTP_200_OK)
