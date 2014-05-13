#-*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from Crypto.Cipher import AES
from newcar.models import Maker, Car, Trim, Nation, Address, Buy, Dealer
from newcar.forms import BuyNewForm, BuyForm, BuyModifyForm, BuyDoneForm, UserForm
from newcar.forms import DealerNewForm
from newcar.serializers import MakerSerializer, CarSerializer, TrimSerializer, AddressSerializer
from newcar.serializers import BuyNewSerializer, LoginSerializer, BuyModifySerializer, BuySerializer
from newcar.serializers import BuyListFreeSerializer, NewUserSerializer, NewDealerSerializer
import pdb;

class Index(APIView):
  def get(self, request, format=None):
    return Response(template_name='index.html')

# Product List View
class CarList(APIView):
  def get(self, request, mid='0', cid='0', tid='0', format=None):
#    pdb.set_trace()
    # return makers if no query condition
    if (mid == '0'):
      makers = Maker.objects.all().order_by('id')
      if request.accepted_renderer.format == 'html':
        data = {'makers': makers}
        return Response(data, template_name='list_maker.html')
      else:
        serializer = MakerSerializer(makers, many=True)
        return Response(serializer.data)
    # return cars if maker is given
    elif (mid <> '0' and cid == '0'):
      maker = Maker.objects.filter(id=mid)
      cars = Car.objects.filter(maker=maker).order_by('id')
      if request.accepted_renderer.format == 'html':
        data = {'cars': cars}
        return Response(data, template_name='list_car.html')
      else:
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)
    # return trims if maker & car is given
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


# Address List View
class AddressList(APIView):
  def get(self, request, nid='0', format=None):
#    pdb.set_trace()
    if (nid == '0'):
      return Response(data, template_name='list_address.html')
    else:
      nation = Nation.objects.get(id=nid)
      address = Address.objects.filter(nation=nation).order_by('id')
      if request.accepted_renderer.format == 'html':
        data = {'addresses': address}
        return Response(data, template_name='list_address.html')
      else:
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)


# Register new buy reqeust view
class BuyNew(APIView):
  def send_email(self, bid, to):
    subject = 'Confirm message from hcar'
    text_content = 'This is important message.'
    html_content = render_to_string('mail_confirm_buy.html', {'id': bid})
    send_mail(subject, html_content, 'customer@coche.dnip.net', [to])

  # GET 
  def get(self, request, format=None):
    if request.accepted_renderer.format == 'html':
      user_form = UserForm()
      buy_form = BuyNewForm()
      data = {'user_form': user_form, 'buy_form': buy_form}
      return Response(data, template_name='consumer_request_get.html')
    else:
      data = "GET not allowed"
      respStatus = status.HTTP_400_BAD_REQUEST
      return Response(data, status = respStatus)

  # POST 
  def post(self, request, format=None):
    pdb.set_trace()
    # html POST 
    if request.accepted_renderer.format == 'html':
      user_form = UserForm(request.POST)
      buy_form = BuyForm(request.POST)
      # check form's validity
      if user_form.is_valid() and buy_form.is_valid():
        # check former undone request with same email
        old_users = User.objects.filter(email=user_form.cleaned_data['email'])
        #old_reqs = Buy.objects.filter(email=form.cleaned_data['email']).filter(is_done=False)
        if (old_users.count() > 0):
          data = {'msg':'save failed. same email exists', 'errcode':'101'}
          resp_status = status.HTTP_409_CONFLICT
        # send confirm mail after save
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
      # invalid form
      else:
        msg = 'invalid form'
        if not user_form.is_valid():
          msg += ' - ' + str(user_form.errors)
        if not buy_form.is_valid():
          msg += ' - ' + str(dealer_form.errors)
        data = {'msg':msg, 'errcode':'103'}
        resp_status = status.HTTP_400_BAD_REQUEST
      return Response(data, status = resp_status, template_name='consumer_request_result.html')

    # Mobile POST
    else:
      user = NewUserSerializer(data=request.DATA)
      buy = BuyNewSerializer(data=request.DATA)
      if user.is_valid() and buy.is_valid():
        # check former undone request with same email
        old_users = User.objects.filter(email=request.DATA['email'])
        #oldReqs = Buy.objects.filter(email=serializer.data['email']).filter(is_done=False)
        if (old_users.count() > 0):
          data = {'msg':'save failed. same email exists', 'errcode':'101'}
          resp_status = status.HTTP_409_CONFLICT
        # send confirm mail after save
        else:
          try:
            saved_user = user.save()
            saved_user.is_active = False
            saved_user.set_password(saved_user.password)
            saved_user.save()
            saved_buy = buy.save()
            saved_buy.user = saved_user
            saved_buy.cellphone = saved_buy.cellphone.translate({ord('-'):None})
            saved_buy.save()
          except StandardError:
            if not saved_user == None:
              User.objects.filter(id = saved_user.id).delete()
            resp_status = status.HTTP_400_BAD_REQUEST
          else:
            self.send_email(saved_buy.id, saved_user.email)
            data = {'msg':'saved', 'errcode':'000'}
            resp_status = status.HTTP_201_CREATED
      else:
        data = {'msg':'invalid request', 'errcode':'102'}
        resp_status = status.HTTP_400_BAD_REQUEST

      return Response(data, status = resp_status)


# View : Confirm Buy request
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
    return Response(data, status = resp_status, template_name='confirm_result.html')


# View : query my request
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
#    pdb.set_trace()
    # html POST 
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

    # Mobile POST 
    else:
      user_raw = LoginSerializer(request.DATA)
      user = User.objects.filter(is_active=True).filter(email=user_raw.data['email'])
      if user:
        consumer = authenticate(username=user[0].username, password=user_raw.data['password'])
      if user and consumer:
        user = user[0]
        buy = Buy.objects.get(user_id=consumer.id)
        if buy:
          if buy.is_confirmed:
            login(request, consumer)
            resp_code = '000'
            resp_status = status.HTTP_200_OK
            data = BuySerializer(buy).data
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
      return Response(data, status = resp_status)


# View : Modify request
class BuyModify(APIView):
  def get(self, request, bid, format=None):
#    pdb.set_trace()
    if request.accepted_renderer.format == 'html':
      if not request.user.is_authenticated():
        data = {'msg':'Query first', 'error_code':'999'}
        resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status, template_name='consumer_modify_get.html')
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
      return Response(data, template_name='consumer_modify_get.html')
    else:
      data = "GET not allowed"
      resp_status = status.HTTP_400_BAD_REQUEST
      return Response(data, status = resp_status)

  def post(self, request, bid, format=None):
    pdb.set_trace()
    # html POST
    if request.accepted_renderer.format == 'html':
      if not request.user.is_authenticated():
        data = {'msg':'Query first', 'error_code':'999'}
        resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status, template_name='consumer_modify_result.html')

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
        return Response(data, status=resp_status, template_name='consumer_modify_result.html')
      else:
        data = {'msg':'invalid form'}
        resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status, template_name='consumer_modify_result.html')

    # Mobile POST
    else:
      if not request.user.is_authenticated():
        data = {'msg':'Query first', 'error_code':'999'}
        resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status)
      changed_buy = BuyModifySerializer(data=request.DATA)
      resp_status = status.HTTP_200_OK
      return Response(status = resp_status)


# View : done(finish) request
class BuyDone(APIView):
  def get(self, request, bid, format=None):
#    pdb.set_trace()
    if request.accepted_renderer.format == 'html':
      if not request.user.is_authenticated():
        data = {'msg':'Query first', 'error_code':'999'}
        resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status, template_name='consumer_modify_get.html')
      buy = Buy.objects.get(id=bid)
      if buy:
        form = BuyDoneForm()
        data = {'buy':buy, 'form':form}
        data['bid']= bid
      else:
        data = {'msg':'Buy request does not exists'}
        resp_status = status.HTTP_400_BAD_REQUEST
      return Response(data, template_name='consumer_done_get.html')
    else:
      data = "GET not allowed"
      resp_status = status.HTTP_400_BAD_REQUEST
      return Response(data, status = resp_status)

  def post(self, request, bid, format=None):
    pdb.set_trace()
    # html POST
    if request.accepted_renderer.format == 'html':
      if not request.user.is_authenticated():
        data = {'msg':'Query first', 'error_code':'999'}
        resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status, template_name='consumer_done_result.html')

      form = BuyDoneForm(request.POST)
      if form.is_valid():
        buy = Buy.objects.get(id=bid, is_done=False)
        buy.satisfaction=int(form.data['satisfaction'])
        buy.dealer_email=form.data['dealer_email']
        if buy.dealer_email:
          dealer = Dealer.objects.get(user=User.objects.get(email=buy.dealer_email))
          total_score = dealer.reputation * float(dealer.num_sell) + float(buy.satisfaction)
          dealer.num_sell += 1
          total_score_int = total_score / float(dealer.num_sell) * 100
          dealer.reputation = float(total_score_int) / 100.0
          buy.delaer = dealer
        buy.is_done = True
        buy.done_date = datetime.now()
        buy.save()
        User.objects.filter(id=buy.user.id).delete()
        logout(request)
        resp_status = status.HTTP_200_OK
        data = {'msg':'done'}
        return Response(data, status=resp_status, template_name='consumer_done_result.html')
      else:
        data = {'msg':'invalid form', 'error_code':'888'}
        resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status, template_name='consumer_done_result.html')

    # Mobile POST
    else:
      changed_buy = BuyModifySerializer(data=request.DATA)
      resp_status = status.HTTP_200_OK
      return Response(status = resp_status)





















# preparing AJAX
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















# View : Dealer register
class DealerRegister(APIView):
  def send_email(self, id, to):
    subject = 'Confirm message from hcar'
    text_content = 'This is important message.'
    html_content = render_to_string('mail_confirm_dealer.html', {'id': id})
    send_mail(subject, html_content, 'customer@coche.dnip.net', [to])

  # GET : send form
  def get(self, request, format=None):
    # html GET
    if request.accepted_renderer.format == 'html':
      user_form = UserForm()
      dealer_form = DealerNewForm()
      data = {'user_form': user_form, 'dealer_form': dealer_form}
      return Response(data, template_name='dealer_register_get.html')
    # Mobile GET
    else:
      data = {'msg':"GET not allowed"}
      respStatus = status.HTTP_400_BAD_REQUEST
      return Response(data, status = respStatus)

  # POST
  def post(self, request, format=None):
    pdb.set_trace()
    # html POST
    if request.accepted_renderer.format == 'html':
      is_registered = False
      user_form = UserForm(request.POST)
      dealer_form = DealerNewForm(request.POST)
      # check form's validity
      if user_form.is_valid() and dealer_form.is_valid():
        # check former undone request with same email
        old_users = User.objects.filter(email=user_form.cleaned_data['email'])
        if (old_users.count() > 0):
          msg = 'register failed. same email exists'
          resp_code = '101'
          resp_status = status.HTTP_409_CONFLICT
        else:
          user = user_form.save(commit=False)
          user.is_active = False
          user.set_password(user.password) 
          dealer = dealer_form.save(commit=False)
          user.save()
          dealer.user = user
          dealer.phone = dealer.phone.translate({ord('-'):None})
          dealer.save()
          # send confirm mail after save
          self.send_email(user.id, user.email)
          msg = 'saved'
          resp_code = '000'
          resp_status = status.HTTP_201_CREATED
          is_registered = True
      # invalid form
      else:
        msg = 'invalid form'
        if not user_form.is_valid():
          msg += ' - ' + str(user_form.errors)
        if not dealer_form.is_valid():
          msg += ' - ' + str(dealer_form.errors)
        resp_code = '103'
        resp_status = status.HTTP_400_BAD_REQUEST
      data = {'msg':msg, 'resp code':resp_code}
      return Response(data, status = resp_status, template_name='dealer_register_result.html')

    # Mobile POST
    else:
      #  WANING!! model dealer need used id. client send temporary uid 1
      user = NewUserSerializer(data=request.DATA)
      dealer = NewDealerSerializer(data=request.DATA)
      if user.is_valid() and dealer.is_valid():
        # check former undone request with same email
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
            # send confirm mail after save
            self.send_email(user.id, user.email)
            resp_status = status.HTTP_201_CREATED
      else:
        resp_status = status.HTTP_400_BAD_REQUEST

      return Response(status = resp_status)







# View : confirm dealer
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
    return Response(data, status = resp_status, template_name='confirm_result.html')


# View : dealer login
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

  # GET
  def get(self, request, format=None):
    # HTML
    if request.accepted_renderer.format == 'html':
      if request.user.is_authenticated():
        msg = 'already logged in by [' + request.user.username + ']'
        resp_code = '101'
        resp_status = status.HTTP_400_BAD_REQUEST
        data = {'msg':msg, 'resp code':resp_code}
        return Response(data, status = resp_status, template_name='dealer_login_result.html')
      else:
        return Response(template_name='dealer_login_get.html')
    # Mobile
    else:
      data = {'msg':"GET not allowed"}
      resp_status = status.HTTP_400_BAD_REQUEST
      return Response(data, status = resp_status)

  # POST
  def post(self, request, format=None):
    pdb.set_trace()
    # HTML
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
      return Response(data, status = resp_status, template_name='dealer_login_result.html')

    # Mobile
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


# View : dealer logout
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
      return Response(data, status = resp_status, template_name='dealer_logout_result.html')
    else:
      return Response(status=status.HTTP_200_OK)


# View : search requests for free
class BuyListFree(APIView):
  def get(self, request, mid, cid='0', addr1='ANY', format=None):
#    pdb.set_trace()
    # HTML
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
      return Response(data, status = resp_status, template_name='dealer_list_result.html')
      
    # Mobile
    else:
      return Response(status=status.HTTP_200_OK)
