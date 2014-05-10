#-*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from Crypto.Cipher import AES
from newcar.models import Maker, Car, Trim, Nation, Address, Buy, Dealer
from newcar.forms import BuyNewForm, BuyForm, BuyModifyForm, UserForm, DealerForm
from newcar.serializers import MakerSerializer, CarSerializer, TrimSerializer, AddressSerializer
from newcar.serializers import BuyNewSerializer, BuyModifySerializer
from newcar.serializers import BuyListFreeSerializer, NewUserSerializer, NewDealerSerializer
import pdb;

class Index(APIView):
  def get(self, request, format=None):
    return Response(template_name='index.html')

# 제조사 및 자동차 리스트를 가져오는 REST 뷰
class CarList(APIView):
  def get(self, request, mid='0', cid='0', tid='0', format=None):
#    pdb.set_trace()
    # 아무 조건도 없다면 메이커 명을 리턴
    if (mid == '0'):
      makers = Maker.objects.all().order_by('id')
      if request.accepted_renderer.format == 'html':
        data = {'makers': makers}
        return Response(data, template_name='list_maker.html')
      else:
        serializer = MakerSerializer(makers, many=True)
        return Response(serializer.data)
    # 메이커명이 주어졌다면 자동차명을 리턴
    elif (mid <> '0' and cid == '0'):
      maker = Maker.objects.filter(id=mid)
      cars = Car.objects.filter(maker=maker).order_by('id')
      if request.accepted_renderer.format == 'html':
        data = {'cars': cars}
        return Response(data, template_name='list_car.html')
      else:
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)
    # 메이커명과 자동차명이 주어졌다면 사양을 리턴
    elif (mid <> '0' and cid <> '0' and tid == '0'):
      maker = Maker.objects.filter(id=mid).order_by('id')
      car = Car.objects.filter(maker=maker, id=cid)
      trims = Trim.objects.filter(car=car).order_by('id')
      if request.accepted_renderer.format == 'html':
        data = {'trims': trims}
        return Response(data, template_name='list_trim.html')
      else:
        serializer = TrimSerializer(trims, many=True)
        return Response(serializer.data)


# 주소요청 뷰
class AddressList(APIView):
  def get(self, request, nid='0', format=None):
#    pdb.set_trace()
    if (nid == '0'):
      return Response(data, template_name='list_address.html')
    else:
      nation = Nation.objects.get(nid=nid)
      address = Address.objects.filter(nid=nation).order_by('aid')
      if request.accepted_renderer.format == 'html':
        data = {'addresses': address}
        return Response(data, template_name='list_address.html')
      else:
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)


# 구매요청 등록 뷰
class BuyNew(APIView):
  def send_email(self, bid, to):
    subject = 'Confirm message from hcar'
    text_content = 'This is important message.'
    html_content = render_to_string('html_buy_confirm.html', {'id': bid})
    send_mail(subject, html_content, 'kshong@coche.dnip.net', [to])

  # GET 구매요청
  def get(self, request, format=None):
    if request.accepted_renderer.format == 'html':
      user_form = UserForm()
      buy_form = BuyNewForm()
      data = {'user_form': user_form, 'buy_form': buy_form}
      return Response(data, template_name='buyrequest_get.html')
    else:
      data = "GET not allowed"
      respStatus = status.HTTP_400_BAD_REQUEST
      return Response(data, status = respStatus)

  # POST 구매요청
  def post(self, request, format=None):
    pdb.set_trace()
    # html POST 접근일 경우
    if request.accepted_renderer.format == 'html':
      user_form = UserForm(request.POST)
      buy_form = BuyForm(request.POST)
      # form 확인
      if user_form.is_valid() and buy_form.is_valid():
        # 동일 이메일로 완료되지 않은 구매 요청이 있는지 확인
        old_users = User.objects.filter(email=user_form.cleaned_data['email'])
        #old_reqs = Buy.objects.filter(email=form.cleaned_data['email']).filter(is_done=False)
        if (old_users.count() > 0):
          data = {'msg':'save failed. same email exists', 'errcode':'101'}
          resp_status = status.HTTP_409_CONFLICT
        # 저장후 구매 요청 확인 메일 송신
        else:
          try:
            user = user_form.save(commit=False)
            user.is_active = False
            user.set_password(user.password)
            buy = buy_form.save(commit=False)
            user.save()
            buy.user = user
            buy.cellphone = buy.cellphone.translate({ord('-'):None})
            buy.save()
          except StandardError:
            if not user == None:
              User.objects.filter(id = user.id).delete()
            resp_status = status.HTTP_400_BAD_REQUEST
          else:
            self.send_email(buy.id, user.email)
            data = {'msg':'saved', 'errcode':'000'}
            resp_status = status.HTTP_201_CREATED
      # invalid form일 경우
      else:
        msg = 'invalid form'
        if not user_form.is_valid():
          msg += ' - ' + str(user_form.errors)
        if not buy_form.is_valid():
          msg += ' - ' + str(dealer_form.errors)
        data = {'msg':msg, 'errcode':'103'}
        resp_status = status.HTTP_400_BAD_REQUEST
      return Response(data, status = resp_status, template_name='buyrequest_result.html')

    # 모바일 POST 접근일경우
    else:
      user = NewUserSerializer(data=request.DATA)
      buy = BuyNewSerializer(data=request.DATA)
      if user.is_valid() and buy.is_valid():
        # 동일 이메일로 완료되지 않은 구매 요청이 있는지 확인
        old_users = User.objects.filter(email=request.DATA['email'])
        #oldReqs = Buy.objects.filter(email=serializer.data['email']).filter(is_done=False)
        if (old_users.count() > 0):
          data = {'msg':'save failed. same email exists', 'errcode':'101'}
          resp_status = status.HTTP_409_CONFLICT
        # 저장후 구매 요청 확인 메일 송신
        else:
          try:
            user.save()
            user.is_active = False
            user.set_password(user.password)
            user.save()
            buy.save()
            buy.user = user
            buy.cellphone = buy.cellphone.translate({ord('-'):None})
            buy.save()
          except StandardError:
            if not user == None:
              User.objects.filter(id = user.id).delete()
            resp_status = status.HTTP_400_BAD_REQUEST
          else:
            # 저장후 구매요청 확인 메일 송신
            self.send_email(buy.id, user.email)
            data = {'msg':'saved', 'errcode':'000'}
            resp_status = status.HTTP_201_CREATED
      else:
        data = {'msg':'invalid request', 'errcode':'102'}
        resp_status = status.HTTP_400_BAD_REQUEST

      return Response(data, status = resp_status)


# 구매요청 검증 뷰
class BuyConfirm(APIView):
  def get(self, request, bid, format=None):
    resp_status = status.HTTP_200_OK
    if (int(bid) <= 0):
      data = {'msg':'CONFIRM ERROR'}
    else:
      try:
        buy = Buy.objects.get(id=bid)
        if (buy.is_confirmed == True):
          data = {'msg':'ALREADY CONFIRMED'}
        else:
          user = buy.user
          buy.is_confirmed = True
          user.is_active = True
          buy.save()
          user.save()
          data = {'msg':'CONFIRMED'}
      except Buy.DoesNotExist:
        if user.is_active:
          user.is_active=False
          user.save()
        if buy.is_confirmed:
          buy.is_confirmed=False
          buy.save()
        resp_status = status.HTTP_400_BAD_REQUEST
        data = {'msg':'BAD REQUEST'}
    return Response(data, status = resp_status, template_name='confirm.html')


# 구매요청 변경을 위한 조회
class BuyQuery(APIView):
  def get(self, request, format=None):
    if request.accepted_renderer.format == 'html':
      if request.user.is_authenticated():
        logout(request)
      return Response(template_name='consumer_query_get.html')
    else:
      data = "GET not allowed"
      resp_status = status.HTTP_400_BAD_REQUEST
      return Response(data, status = resp_status)
 
  def post(self, request, format=None):
    pdb.set_trace()
    # html POST 접근일 경우
    if request.accepted_renderer.format == 'html':
      data = {}
      email = request.POST['email']
      password = request.POST['password']
      user = User.objects.filter(is_active=True).filter(email=email)
      if user:
        consumer = authenticate(username=user[0].username, password=password)
      if user and consumer:
        user = user[0]
        buy = Buy.objects.get(user_id=consumer.id)
        if buy:
          if buy.is_confirmed:
            login(request, consumer)
            resp_code = '000'
            resp_status = status.HTTP_200_OK
            data = {'buy':buy, 'resp_code':resp_code}
          else:
            msg = 'your request not confirmed yet'
            resp_code = '101'
            resp_status = status.HTTP_400_BAD_REQUEST
            data = {'msg':msg, 'resp_code':resp_code}
        else:
          msg = 'no buy request'
          resp_code = '101'
          resp_status = status.HTTP_400_BAD_REQUEST
          data = {'msg':msg, 'resp_code':resp_code}
      else:
        msg = 'invalid email/password'
        resp_code = '101'
        resp_status = status.HTTP_400_BAD_REQUEST
        data = {'msg':msg, 'resp_code':resp_code}
      return Response(data, status = resp_status, template_name='consumer_query_result.html')

    # 모바일 POST 접근일경우
    else:
      data = {}
      email = request.POST['email']
      password = request.POST['password']
      user = User.objects.filter(is_active=True).get(email=email)
      consumer = authenticate(username=user.username, password=password)
      if consumer:
        buy = Buy.objects.get(user_id=consumer.id)
      else:
        resp_status = status.HTTP_400_BAD_REQUEST
      return Response(status = resp_status)


# 구매요청 변경
class BuyModify(APIView):
  def post(self, request, bid, format=None):
#    pdb.set_trace()
    # html 접근일 경우
    if request.accepted_renderer.format == 'html':
      if not request.user.is_authenticated():
        data = {'msg':'Query first', 'error_code':'999'}
        resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status, template_name='buychange_result.html')

      changed_form = BuyModifyForm(request.POST)
      if changed_form.is_valid():
        orig_buy = Buy.objects.get(id=bid, is_done=False)
        orig_buy.is_done = request.POST.get('is_cancel', False)
        new_form = BuyModifyForm(request.POST, instance=orig_buy)
        buy = new_form.save()
        #values = BuyModifySerializer(buy).data.items()
        #data = {'buy':values}
        data = {'buy':buy}
        resp_status = status.HTTP_200_OK
        logout(request)
        if buy.is_cancel:
          User.objects.filter(id=buy.user.id).delete()
        return Response(data, status=resp_status, template_name='buychange_result.html')
      else:
        data = {'msg':'invalid form'}
        resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status, template_name='buychange_result.html')

    # 모바일 접근일 경우
    else:
      changed_buy = BuyModifySerializer(data=request.DATA)
      resp_status = status.HTTP_200_OK
      return Response(status = resp_status)

  def get(self, request, bid, format=None):
#    pdb.set_trace()
    if request.accepted_renderer.format == 'html':
      if not request.user.is_authenticated():
        data = {'msg':'Query first', 'error_code':'999'}
        resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status, template_name='buychange_get.html')
      buy = Buy.objects.get(id=bid)
      if buy:
        initial_value = BuyModifySerializer(buy)
        form = BuyModifyForm(initial=initial_value.data)
        data = {'buy_form':form}
        data['msg'] = 'Name : '+buy.user.username+'<'+buy.user.email+'>'
        data['bid']= bid
      else:
        data = {'msg':'Buy request does not exists'}
        resp_status = status.HTTP_400_BAD_REQUEST
      return Response(data, template_name='buychange_get.html')
    else:
      data = "GET not allowed"
      resp_status = status.HTTP_400_BAD_REQUEST
      return Response(data, status = resp_status)


# 구매요청 완료
class BuyDone(APIView):
  def get(self, request, bid, format=None):
    if request.accepted_renderer.format == 'html':
      if not request.user.is_authenticated():
        data = {'msg':'Query first', 'error_code':'999'}
        resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status, template_name='buychange_get.html')
      buy = Buy.objects.get(id=bid)
      if buy:
        initial_value = BuyModifySerializer(buy)
        form = BuyModifyForm(initial=initial_value.data)
        data = {'buy_form':form}
        data['msg'] = 'Name : '+buy.user.username+'<'+buy.user.email+'>'
        data['bid']= bid
      else:
        data = {'msg':'Buy request does not exists'}
        resp_status = status.HTTP_400_BAD_REQUEST
      return Response(data, template_name='buychange_get.html')
    else:
      data = "GET not allowed"
      resp_status = status.HTTP_400_BAD_REQUEST
      return Response(data, status = resp_status)






















# 구매요청 시 차종을 ajax로 선택하게 하기 위한 뷰
class GetCID(APIView):
  def get(self, request):
    pdb.set_trace()
    maker = Maker.get_object_or_404(id=request.GET.get('mid', None))
    resp = ",".join(maker.car_set.values_list('name', flat=True))
    return HttpResponse(resp)
  def post(self, request):
    pdb.set_trace()
    resp = ",".join(maker.car_set.values_list('name', flat=True))
    return HttpResponse(resp)















# 딜러 회원 가입
class DealerRegister(APIView):
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
      return Response(data, template_name='register_get.html')
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
          user.set_password(user.password)  # 비밀번호 해시
          dealer = dealer_form.save(commit=False)
          user.save()
          dealer.user = user
          dealer.phone = dealer.phone.translate({ord('-'):None})
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
      # Dealer 모델은 user id가 반드시 필요하여 클라이언트에서 임시로 uid를 1로 올림
      user = NewUserSerializer(data=request.DATA)
      dealer = NewDealerSerializer(data=request.DATA)
      if user.is_valid() and dealer.is_valid():
        # 동일 이메일로 완료되지 않은 구매 요청이 있는지 확인
        old_users = User.objects.filter(email=request.DATA['email'])
        if (old_users.count() > 0):
          resp_status = status.HTTP_409_CONFLICT
        else:
          try:
            user.save()
            user.is_active = False
            user.set_password(user.password)
            user.save()
            dealer.save()
            dealer.user = user
            dealer.phone = dealer.phone.translate({ord('-'):None})
            dealer.save()
            #user = user_serializer.save()
            #user.is_active = False
            #user.set_password(user.password)
            #user.save()
            #dealer = dealer_serializer.save()
            #dealer.user = user
            #dealer.save()
          except StandardError:
            if not user == None:
              User.objects.filter(id = user.id).delete()
            resp_status = status.HTTP_400_BAD_REQUEST
          else:
            # 저장후 딜러 확인 메일 송신
            self.send_email(user.id, user.email)
            resp_status = status.HTTP_201_CREATED
      else:
        resp_status = status.HTTP_400_BAD_REQUEST

      return Response(status = resp_status)







# 딜러 검증 뷰
class DealerConfirm(APIView):
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
        resp_status = status.HTTP_400_BAD_REQUEST
        data = {'msg':'BAD REQUEST'}
    return Response(data, status = resp_status, template_name='confirm.html')


# 딜러 로그인 뷰
class DealerLogin(APIView):
  def _lazysecret(self, secret, blocksize=32, padding='}'):
    """pads secret if not legal AES block size (16, 24, 32)"""
    if not len(secret) in (16, 24, 32):
      return secret + (blocksize - len(secret)) * padding
    return secret

  def decrypt(self, ciphertext, secret, lazy=True):
    """decrypt ciphertext with secret
    ciphertext  - encrypted content to decrypt
    secret    - secret to decrypt ciphertext
    lazy    - pad secret if less than legal blocksize (default: True)
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
      data = "GET not allowed"
      resp_status = status.HTTP_400_BAD_REQUEST
      return Response(data, status = resp_status)

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
          msg = 'login succeed'
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
#      rawpass = request.DATA['password']
#      password = self.decrypt(rawpass, '12345678901234567890123456789012')
      password = request.DATA['password']
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
class DealerLogout(APIView):
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
#    pdb.set_trace()
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
          buy_list = Buy.objects.filter(maker_id=mid).filter(is_confirmed=True)
        else:
          buy_list = Buy.objects.filter(car_id=cid).filter(is_confirmed=True)
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
