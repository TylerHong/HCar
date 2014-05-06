#-*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Crypto.Cipher import AES
from newcar.models import Maker, Car, Trim, Buy, Dealer
from newcar.forms import BuyForm, UserForm, DealerForm
from newcar.serializers import MakerSerializer, CarSerializer, TrimSerializer, BuyRequestSerializer, BuyListFreeSerializer
import pdb;


# 제조사 및 자동차 리스트를 가져오는 REST 뷰
class CarList(APIView):
    def get(self, request, mid='0', cid='0', tid='0', format=None):
#        pdb.set_trace()
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
        elif (mid <> '0' and cid == '0'):
            maker = Maker.objects.filter(mid=mid)
            cars = Car.objects.filter(mid=maker).order_by('cid')
            if request.accepted_renderer.format == 'html':
                data = {'cars': cars}
                return Response(data, template_name='list_car.html')
            else:
                serializer = CarSerializer(cars, many=True)
                return Response(serializer.data)
        # 메이커명과 자동차명이 주어졌다면 사양을 리턴
        elif (mid <> '0' and cid <> '0' and tid == '0'):
            maker = Maker.objects.filter(mid=mid).order_by('mid')
            car = Car.objects.filter(mid=maker, cid=cid)
            trims = Trim.objects.filter(cid=car).order_by('tid')
            if request.accepted_renderer.format == 'html':
                data = {'trims': trims}
                return Response(data, template_name='list_trim.html')
            else:
                serializer = TrimSerializer(trims, many=True)
                return Response(serializer.data)

# 구매요청 등록 뷰
class BuyRequest(APIView):
    def send_email(self, bid, to):
        subject = 'Confirm message from hcar'
        text_content = 'This is important message.'
        html_content = render_to_string('html_buy_confirm.html', {'id': bid})
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




# 딜러 회원가입 뷰
class Register(APIView):
    def send_email(self, id, to):
        subject = 'Confirm message from hcar'
        text_content = 'This is important message.'
        html_content = render_to_string('html_dealer_confirm.html', {'id': id})
        send_mail(subject, html_content, 'kshong@coche.dnip.net', [to])

    def get(self, request, format=None):
        if request.accepted_renderer.format == 'html':
            user_form = UserForm()
            dealer_form = DealerForm()
            data = {'user_form': user_form, 'dealer_form': dealer_form}
            return Response(data, template_name='register_post.html')
        else:
            data = "GET not allowed"
            respStatus = status.HTTP_400_BAD_REQUEST
            return Response(data, status = respStatus)

    def post(self, request, format=None):
        pdb.set_trace()
        # html 접근일 경우
        if request.accepted_renderer.format == 'html':
            is_registered = False
            user_form = UserForm(request.POST)
            dealer_form = DealerForm(request.POST)
            # form 확인
            if user_form.is_valid() and dealer_form.is_valid():
                # 동일 이메일로 등록된 딜러가 있는지 확인
                old_users = User.objects.filter(email=user_form.cleaned_data['email'])
                if (old_users.count() > 0):
                    msg = 'register failed. same email exists'
                    resp_code = '101'
                    resp_status = status.HTTP_409_CONFLICT
                else:
                    user = user_form.save(commit=False)
                    user.is_active = False
                    user.set_password(user.password)    # 비밀번호 해시
                    dealer = dealer_form.save(commit=False)
                    user.save()
                    dealer.user = user
                    dealer.save()
                    # 저장후 딜러 확인 메일 송신
                    self.send_email(user.id, user.email)
                    msg = 'saved'
                    resp_code = '000'
                    resp_status = status.HTTP_201_CREATED
                    is_registered = True
            # invalid form 일 경우
            else:
                msg = 'invalid form'
                if not user_form.is_valid():
                    msg += ' - ' + str(user_form.errors)
                if not dealer_form.is_valid():
                    msg += ' - ' + str(dealer_form.errors)
                resp_code = '103'
                resp_status = status.HTTP_400_BAD_REQUEST
            data = {'msg':msg, 'resp code':resp_code}
            return Response(data, status = resp_status, template_name='register_result.html')

        # html 이외 접근일경우 (모바일)
        else:
            return Response(data, status = respStatus)

# 딜러 검증 뷰
class ConfirmDealer(APIView):
    def get(self, request, id, format=None):
        respStatus = status.HTTP_200_OK
        if (int(id) <= 0):
            data = {'msg':'CONFIRM ERROR'}
        else:
            try:
                dealer = Dealer.objects.get(user_id=id)
                if (dealer.is_confirmed == True):
                    data = {'msg':'ALREADY CONFIRMED'}
                else:
                    dealer.is_confirmed = True
                    user = dealer.user
                    user.is_active = True
                    user.save()
                    dealer.save()
                    data = {'msg':'CONFIRMED'}
            except Dealer.DoesNotExist:
                respStatus = status.HTTP_400_BAD_REQUEST
                data = {'msg':'BAD REQUEST'}
        return Response(data, status = respStatus, template_name='confirm.html')

# 딜러 로그인 뷰
class Login(APIView):
    def _lazysecret(self, secret, blocksize=32, padding='}'):
        """pads secret if not legal AES block size (16, 24, 32)"""
        if not len(secret) in (16, 24, 32):
            return secret + (blocksize - len(secret)) * padding
        return secret

    def decrypt(self, ciphertext, secret, lazy=True):
        """decrypt ciphertext with secret
        ciphertext  - encrypted content to decrypt
        secret      - secret to decrypt ciphertext
        lazy        - pad secret if less than legal blocksize (default: True)
        returns plaintext
        """
        secret = self._lazysecret(secret) if lazy else secret
        encobj = AES.new(secret, AES.MODE_CFB)
        plaintext = encobj.decrypt(ciphertext)
        return plaintext

    def get(self, request, format=None):
        if request.accepted_renderer.format == 'html':
            if request.user.is_authenticated():
                msg = 'already logged in by [' + request.user.username + ']'
                resp_code = '101'
                resp_status = status.HTTP_400_BAD_REQUEST
                data = {'msg':msg, 'resp code':resp_code}
                return Response(data, status = resp_status, template_name='login_result.html')
            else:
                return Response(template_name='login.html')
        else:
            return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        pdb.set_trace()
        # html 접근일 경우
        if request.accepted_renderer.format == 'html':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                dealer = Dealer.objects.get(user_id=user.id)
                if dealer and user.is_active and dealer.is_confirmed:
                    login(request, user)
                    msg = 'login succedd'
                    resp_code = '000'
                    resp_status = status.HTTP_200_OK
                else:
                    msg = 'inactive user'
                    resp_code = '101'
                    resp_status = status.HTTP_400_BAD_REQUEST
            else:
                msg = 'invalid user/password'
                resp_code = '101'
                resp_status = status.HTTP_400_BAD_REQUEST
            data = {'msg':msg, 'resp code':resp_code}
            return Response(data, status = resp_status, template_name='login_result.html')

        # 모바일 접근일경우
        else:
            username = request.DATA['username']
            rawpass = request.DATA['password']
            password = self.decrypt(rawpass, 'coche')
            user = authenticate(username=username, password=password)
            if user:
                dealer = Dealer.objects.get(user_id=user.id)
                if dealer and user.is_active and dealer.is_confirmed:
                    login(request, user)
                    resp_status = status.HTTP_200_OK
                else:
                    resp_status = status.HTTP_400_BAD_REQUEST
            else:
                resp_status = status.HTTP_400_BAD_REQUEST
            return Response(status = resp_status)


# 딜러 로그아웃 뷰
class Logout(APIView):
    def get(self, request, format=None):
        if request.accepted_renderer.format == 'html':
            if request.user.is_authenticated():
                logout(request)
                msg = 'Logged out.'
                resp_code = '000'
                resp_status = status.HTTP_200_OK
            else:
                msg = 'You must login first.'
                resp_code = '101'
                resp_status = status.HTTP_400_BAD_REQUEST
            data = {'msg':msg, 'resp code':resp_code}
            return Response(data, status = resp_status, template_name='logout_result.html')
        else:
            return Response(status=status.HTTP_200_OK)


# 구매요청 검색 뷰 for anyone
class BuyListFree(APIView):
    def get(self, request, mid, cid='0', addr1='ANY', format=None):
        pdb.set_trace()
        # HTML 요청일 경우
        if request.accepted_renderer.format == 'html':
            if (int(mid) <= 0):
                msg = 'invalid mid'
                resp_code = '202'
                resp_status = status.HTTP_400_BAD_REQUEST
                data = {'msg':msg, 'resp code':resp_code}
            elif (int(cid) < 0):
                msg = 'invalid cid'
                resp_code = '203'
                resp_status = status.HTTP_400_BAD_REQUEST
                data = {'msg':msg, 'resp code':resp_code}
            else:
                if (int(cid) == 0):
                    buy_list = Buy.objects.filter(mid_id=mid).filter(is_confirmed=True)
                else:
                    buy_list = Buy.objects.filter(cid_id=cid).filter(is_confirmed=True)
                if (buy_list.count() > 0 and addr1 <> 'ANY'):
                    buy_list = buy_list.filter(addr1__contains=addr1)
                if (buy_list.count() == 0):
                    msg = 'no data in such condition'
                    resp_code = '201'
                    resp_status = status.HTTP_400_BAD_REQUEST
                    data = {'msg':msg, 'resp code':resp_code}
                elif (buy_list.count() == 1):
                    serializer = BuyListFreeSerializer(buy_list)
                    resp_status = status.HTTP_200_OK
                    #data = {'buys':serializer.data}
                    data = {'buys':buy_list}
                else:
                    serializer = BuyListFreeSerializer(buy_list, many=True)
                    resp_status = status.HTTP_200_OK
                    data = {'buys':serializer.data}
            return Response(data, status = resp_status, template_name='buylist_result.html')
            
        # 모바일 요청일경우
        else:
            return Response(status=status.HTTP_200_OK)
