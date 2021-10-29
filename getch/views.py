from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password
from allauth.account.utils import perform_login
from urllib import parse
# from django.db.models import F
# from django.db.models import Q
from django.db.models import F, Q, Sum, Count, Case, When
from django.template.loader import render_to_string
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
import getch.models as m
from allauth.account.views import LoginView, LogoutView
from allauth.socialaccount.helpers import complete_social_signup, complete_social_login
from allauth.socialaccount.models import SocialAccount, SocialLogin
# import getch.serializers as ser
# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from notifications.signals import notify
import random
import os
import json
import collections
from datetime import datetime, date, timedelta
# from gensim.models import Doc2Vec
from django.utils import timezone
# from slacker import Slacker
from slack_sdk import WebClient

import base64
import hashlib
import hmac
import time
import requests
import pandas as pd


# bgrs = []

labels = {
    'gender': list(m.Genderlabel.objects.order_by('key').values('id', 'label')),
    'age': list(m.Agelabel.objects.order_by('key').values('id', 'label')),
    # 'body': list(m.Bodylabel.objects.order_by('key').values('id', 'label')),
    'style': list(m.Stylelabel.objects.order_by('key').values('id', 'label')),
    'item': list(m.Itemlabel.objects.order_by('key').values('id', 'label'))
}

context = { 'labels':labels }

def redirect_params(url, params=None):
    response = redirect(url)
    if params:
        query_string = parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response


def test(request):
    return render(request, 'getch/test.html')

def discover(request):
    request.session.save()
    context['entry'] = request.GET.get('entry', None)
    context['id'] = request.GET.get('id', None)
    # context['dongne'] = request.GET.get('dongne', None)
    context['gender'] = request.GET.get('gender', None)
    context['kakao_js_key'] = settings.KAKAO_JS_KEY
    # print(request.user.boo.reward_snapshot)
    return render(request, 'getch/moiber/discover.html', context)


# def policy(request):
#     return render(request, 'getch/policy.html')
#
# def privacy(request):
#     return render(request, 'getch/privacy.html')
#
# def recruit(request):
#     return render(request, 'getch/recruit.html')

def policy(request):
    params = { 'entry': 'policy' }
    return redirect_params('discover', params)


def privacy(request):
    params = { 'entry': 'privacy' }
    return redirect_params('discover', params)


def recruit(request):
    params = { 'entry': 'recruit' }
    return redirect_params('discover', params)


def app_ios(request):
    return redirect('https://itunes.apple.com/app/id1578448720')


def app_android(request):
    return redirect('https://play.google.com/store/apps/details?id=com.moiber.mobileApp')


def load(request, ctx):
    # 처음 로딩할때는 session 객체가 없어서,
    # 이렇게 save()해주면 새로 생기면서 session_key가 만들어진다
    # 즉 로그인 안했을때도 session_key를 쓸수 있다
    # 이후 로그인하면 해당 session_key가 유지되도록 설정: setting에서 SESSION_ENGINE = 'getch.session_backend'
    # 로그아웃 하면, 해당 session이 지워지고, 이 부분의 코드가 다시 실행되면서 새로운 session_key가 생성된다
    # 2021.02.19
    request.session.save()

    # if request.user.is_authenticated:
    #     if request.user.is_staff:
    #         ctx['utype'] = 'staff'
    #     else:
    #         ctx['utype'] = 'general'
    #
    # else:
    #     ctx['utype'] = 'guest'

    return render(request, 'getch/play.html', ctx)

def play(request):
    # hotboos_id = m.Flager.objects.filter(status=10).values('object_id').annotate(nfollowers=Count('object_id')).order_by('-nfollowers')[:5].values_list('id', flat=True)
    # notify.send(request.user, recipient=request.user, verb='you reached level 10')

    # _iboos = m.Flager.objects.filter(status=m.FOLLOW).values('object_id').annotate(nfollowers=Count('object_id')).order_by('-nfollowers')[:10].values_list('object_id', flat=True)

    # print(_flags)

    context['req'] = 0
    return load(request, context)


# def company(request):
#     return HttpResponseRedirect(reverse('discover'))

def company(request):
    params = { 'entry': 'about' }
    return redirect_params('discover', params)

def about(request):
    params = { 'entry': 'about' }
    return redirect_params('discover', params)

def company_recruit(request):
    context['req'] = 2
    return load(request, context)

# def landing(request):
#     return HttpResponseRedirect(reverse('discover'))


def landing(request):
    params = { 'entry': 'landing' }
    return redirect_params('discover', params)
    # request.session.save()
    # context['entry'] = 'landing'
    # return render(request, 'getch/moiber/discover.html', context)

def zthinker(request):
    params = { 'entry': 'zthinker' }
    return redirect_params('discover', params)


def testbed(request):
    params = { 'entry': 'testbed' }
    return redirect_params('discover', params)

# def testbed(request):
#     context['req'] = 5
#     return load(request, context)
#
# def testfeed(request):
#     context['req'] = 6
#     return load(request, context)


# def user_check_signup(request):
#     if request.method=='POST':
#         _email = request.POST.get('email', None)
#
#         if _email:
#             _exist = m.User.objects.filter(email=_email).exists()
#             return JsonResponse({'success':True, 'exist':_exist, 'message':'signup checked successfully'}, safe=False)
#
#         else:
#             return JsonResponse({'success':False, 'message':'something wrong while checking signup'}, safe=False)


# def slack_notify(channel=None, blocks=None):
#     token = 'xoxb-395086725542-2541429028388-i7Gjg4WbFjpZUQqXfioFFuJW'
#     client = WebClient(token=token)
#     client.chat_postMessage(channel="#5-기술-앱봇", blocks=blocks, text='텍스트블라블라')
#
#
# blocks = [{
# 	"type": "section",
# 	"text": {
# 		"type": "mrkdwn",
# 		"text": ">*테스트해봅시당*\n>• Detective Chimp\n>• Bouncing Boy\n>• Aqualad"
# 	}
# }]
#
# slack_notify(channel='#5-기술-앱봇', blocks=blocks)


def make_signature(string):
    secret_key = bytes("0erEPaknjXM1AnKBWW0r0WHKYeFnxsdhewWkbHoC", 'UTF-8')
    string = bytes(string, 'UTF-8')
    string_hmac = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
    string_base64 = base64.b64encode(string_hmac).decode('UTF-8')
    return string_base64


def send_mobile_authkey(request):
    number = request.GET.get('number', None)

    if number == '':
        return JsonResponse({'success':False, 'message':'휴대번호를 입력해주세요'}, safe=False)

    url = "https://sens.apigw.ntruss.com"
    uri = "/sms/v2/services/" + "ncp:sms:kr:270782467605:auth" + "/messages"
    api_url = url + uri
    timestamp = str(int(time.time() * 1000))
    access_key = "uhp30EUaIfhXwU4sB74a"
    string_to_sign = "POST " + uri + "\n" + timestamp + "\n" + access_key
    signature = make_signature(string_to_sign)

    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signature
    }

    auth_num = random.randint(1000, 10000)
    message = f"인증 번호는 {auth_num}입니다. 정확하게 입력해주세요."		# 메세지 내용을 저장
    phone = number		                                        	# 핸드폰 번호를 저장

    body = {
        "type": "SMS",
        "contentType": "COMM",
        "from": "01049103793",
        "content": message,
        "messages": [{"to": phone}]
    }

    body = json.dumps(body)

    # 문자 전송
    response = requests.post(api_url, headers=headers, data=body)

    m.MobileVerifier.objects.create(mobile=number, authkey=auth_num)
    return JsonResponse({'success':True, 'number':number, 'message':'send authkey message successfully'}, safe=False)


def mobile_verify(request):
    mobile = request.GET.get('mobile', None)
    authkey = request.GET.get('authkey', None)

    try:
        _verifier = m.MobileVerifier.objects.filter(mobile=mobile).last()
        # print(_verifier.authkey)

        if _verifier.authkey == int(authkey):
            print(authkey)
            return JsonResponse({'code':0, 'message':'verified successfully'}, safe=False)

        else:
            return JsonResponse({'code':1, 'message':'not verified'}, safe=False)

    except:
        return JsonResponse({'code':2, 'message':'something wrong while verifying authkey'}, safe=False)


def mobile_verify_save(request):
    try:
        user = request.user
        if user.is_authenticated:
            user.mobile_verified = True
            user.save()
            return JsonResponse({'success':True, 'message':'mobile_verified saved successfully'}, safe=False)

        else:
            pass

    except:
        return JsonResponse({'success':False, 'message':'something wrong while saving mobile_verified'}, safe=False)




def signup_email_check(request):
    if request.method == 'POST':
        try:
            _email = request.POST.get('email', None)
            _user = m.User.objects.filter(email=_email).first()

            if _user:
                _boo = _user.boo
                _nick = _boo.nick
                _profilepix = _boo.profile.pix.url
                _socialaccount = _user.socialaccount_set.first()

                if _socialaccount:
                    _provider = _socialaccount.provider
                else:
                    _provider = None

                _existing = { 'email': _email, 'nick': _nick, 'profilepix': _profilepix, 'provider': _provider }
                return JsonResponse({'code':1, 'existing':_existing, 'message':'this email already exists'}, safe=False)

            else:
                return JsonResponse({'code':0, 'message':'possible to use this email'}, safe=False)

        except:
            return JsonResponse({'code':-1, 'message':'something wrong while checking email'}, safe=False)


def kakaotalk_login(request):
    # _user = m.User.objects.create(email='tekk21@tageaglk.cm')
    # _account = SocialAccount.objects.create(user=_user, provider='kakao', uid='11122331')
    # perform_login(request, _user, email_verification='optional')
    # return JsonResponse({'code':-1, 'message':'something wrong while checking email'}, safe=False)

    # sociallogin = SocialLogin(account)
    # complete_social_login(request, sociallogin)

    if request.method == 'POST':
        try:
            _data = request.POST.get('data', None)#; print(type(_data))
            _data = json.loads(_data)#; print(type(_data), _data)
            _email = _data['kakao_account']['email']
            _user = m.User.objects.filter(email=_email).first()

            if _user:
                perform_login(request, _user, email_verification='optional')
                return JsonResponse({'code':0, 'message':'logged in successfully'}, safe=False)

            else:
                _user = m.User.objects.create(email=_email)
                _user.set_unusable_password()
                _user.save()
                _account = SocialAccount.objects.create(user=_user, provider='kakao', uid=_data['id'])
                perform_login(request, _user, email_verification='optional')
                return JsonResponse({'code':1, 'message':'signed up successfully'}, safe=False)


        except:
            return JsonResponse({'code':-1, 'message':'something wrong while kakaotalk logining'}, safe=False)


    # if request.method == 'POST':
    #     try:
    #         _email = request.POST.get('email', None)
    #         _user = m.User.objects.filter(email=_email).first()
    #
    #         if _user:
    #             _socialaccount = _user.socialaccount_set.first()
    #
    #             if _socialaccount:
    #                 _provider = _socialaccount.provider
    #                 _existing = { 'email': _email, 'nick': _nick, 'profilepix': _profilepix, 'provider': _provider }
    #                 return JsonResponse({'code':3, 'existing':_existing, 'message':'the socialacount already exists'}, safe=False)
    #
    #             else:
    #                 return JsonResponse({'code':0, 'message':'no matching kakao account'}, safe=False)
    #
    #         else:
    #             return JsonResponse({'code':1, 'message':'no matching acount'}, safe=False)
    #
    #     except:
    #         return JsonResponse({'code':-1, 'message':'something wrong while logining'}, safe=False)


def email_login(request):
    if request.method == 'POST':
        try:
            _email = request.POST.get('email', None)
            _pw = request.POST.get('pw', None)
            _user = m.User.objects.filter(email=_email).first()

            if _user:
                _boo = _user.boo
                _nick = _boo.nick
                _profilepix = _boo.profile.pix.url
                _socialaccount = _user.socialaccount_set.first()

                if _socialaccount:
                    _provider = _socialaccount.provider
                    _existing = { 'email': _email, 'nick': _nick, 'profilepix': _profilepix, 'provider': _provider }
                    return JsonResponse({'code':3, 'existing':_existing, 'message':'the socialacount already exists'}, safe=False)

                elif check_password(_pw, _user.password):
                    # __user = authenticate(email=_email, password=_pw)
                    # login(request, _user)
                    perform_login(request, _user, email_verification='optional')
                    return JsonResponse({'code':0, 'message':'logged in successfully'}, safe=False)

                else:
                    return JsonResponse({'code':2, 'message':'password check'}, safe=False)

            else:
                return JsonResponse({'code':1, 'message':'no matching acount'}, safe=False)

        except:
            return JsonResponse({'code':-1, 'message':'something wrong while logining'}, safe=False)


def email_signup(request):
    if request.method == 'POST':
        try:
            _email = request.POST.get('email', None)
            _pw = request.POST.get('pw', None)
            _user = m.User.objects.create(email=_email)
            _user.set_password(_pw)
            _user.save()
            perform_login(request, _user, email_verification='optional')
            # print(_user, '*****************')
            return JsonResponse({'success':True, 'message':'signed up successfully'}, safe=False)

        except:
            return JsonResponse({'success':False, 'message':'something wrong while signing-up'}, safe=False)


def signup_setbase(request):
    try:
        user = request.user
        if user.is_authenticated:
            _data = json.loads(request.GET.get('data', None))
            # print(_data)
            user.name = _data['name']
            user.gender = 0 if _data['gender']=='남성' else 1
            user.birth = _data['birth']
            user.address = _data['address']
            user.mobile = _data['mobile']
            user.mobile_verified = _data['mobile_verified']
            user.save()
            # user.notify_on_slack();
            return JsonResponse({'success':True, 'message':'signup setbased successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while signup-setbase'}, safe=False)


def signup_setbase_change(request):
    try:
        user = request.user
        if user.is_authenticated:
            _name = request.POST.get('name', None)
            _gender = request.POST.get('gender', None)#; print(_gender)
            _birth = request.POST.get('birth', None)
            _mobile = request.POST.get('mobile', None)
            _address = request.POST.get('address', None)

            # print(_name, '***********')
            if _name is not None:
                user.name = _name

            if _gender is not None:
                user.gender = 0 if _gender=='남성' else 1

            if _birth is not None:
                user.birth = _birth

            if _mobile is not None:
                user.mobile = _mobile
                user.mobile_verified = False

            if _address is not None:
                user.address = _address

            user.save()
            return JsonResponse({'success':True, 'message':'signup setbase changed successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while signup-setbase change'}, safe=False)



# def notify_shopping(request, trans_id):
#     try:
#         if request.user.is_authenticated:
#             m.Notihistory.add(trans_id)
#             return JsonResponse({'success':True, 'message':'notified successfully'}, safe=False)
#
#         else:
#             return JsonResponse({'success':False, 'message':'something wrong while notifying'}, safe=False)
#
#     except:
#         return JsonResponse({'success':False, 'message':'something wrong while notifying'}, safe=False)



def get_user(request):
    sessionkey = request.session.session_key

    if request.user.is_authenticated:
        if request.user.has_active_boo:
            return JsonResponse({'success':True, 'user':request.user.serialized, 'guestboo':m.Boo.guestboo_serialized(sessionkey)}, safe=False)
        else:
            request.user.create_default_boo()
            return JsonResponse({'success':True, 'user':request.user.serialized, 'first_visit':True, 'guestboo':m.Boo.guestboo_serialized(sessionkey)}, safe=False)

    else:
        return JsonResponse({'success':False, 'guestboo':m.Boo.guestboo_serialized(sessionkey)})


def get_user2(request):
    try:
        if request.user.is_authenticated:
            return JsonResponse({'mode':0, 'user':request.user.serialized2}, safe=False)

        else:
            sessionkey = request.session.session_key
            guestboo = m.Boo.guestboo_serialized(sessionkey)
            return JsonResponse({'mode':1, 'guestboo':guestboo})
            # return JsonResponse({'mode':1, 'guestboo':m.Boo.guestboo_serialized(sessionkey)})

    except:
        return JsonResponse({'mode':-1, 'message':'something wrong while auth'})


    # try:
    #     sessionkey = request.session.session_key
    #     guestboo = m.Boo.guestboo_serialized(sessionkey)
    #
    #     if request.user.is_authenticated:
    #         print('***************')
    #         return JsonResponse({'success':True, 'user':request.user.serialized2, 'guestboo':m.Boo.guestboo_serialized(sessionkey)}, safe=False)
    #
    # except:
    #     print('##############')
    #     return JsonResponse({'success':False, 'guestboo':m.Boo.guestboo_serialized(sessionkey)})


def notice_preset(request):
    nomore_today = request.GET.get('nomore_today', None)

    if nomore_today and request.user.is_authenticated:
        nomore_today = (nomore_today == 'true')

        # print(nomore_today, '*****************')
        request.user.boo.settle(nomore_today=nomore_today)
        return JsonResponse({'success':True, 'nomore_today':nomore_today, 'message':'notice preset successfully'}, safe=False)

    else:
        return JsonResponse({'success':False, 'message':'something wrong while notice presetting'}, safe=False)


def get_iresearches(request):
    # _ires = list(m.Research.iresearches(published_only=False))
    _ires = list(m.Research.iresearches)
    return JsonResponse({'success':True, 'ids':_ires}, safe=False)


# def get_iresearches_onwork(request):
#     _ires = list(m.Research.iresearches_onwork)
#     return JsonResponse({'success':True, 'ids':_ires}, safe=False)


def research_done(request, research_id):
    try:
        if request.user.is_authenticated:
            boo = request.user.boo
            research_id = str(research_id)
            boo.answers[research_id]['finished'] = True
            boo.save()
            return JsonResponse({'success':True, 'message':'research done successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while research done'}, safe=False)



def get_research(request, research_id):
    try:
        _research = m.Research.objects.get(pk=research_id)
        _research = m.ResearchSerializer(_research).data
        return JsonResponse({'success':True, 'content':_research}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_checkingame(request):
    try:
        _research = m.Research.objects.get(pk=13)
        _checkin = _research.researchitem_set.order_by('?').first()
        _checkin = m.ResearchItemSerializer(_checkin).data
        return JsonResponse({'success':True, 'content':_checkin}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_iresearchitems(request, research_id):
    _research = m.Research.objects.get(pk=research_id)
    _iresitems = list(_research.iresearchitems)
    return JsonResponse({'success':True, 'ids':_iresitems}, safe=False)


def get_researchitem(request, researchitem_id):
    try:
        _researchitem = m.ResearchItem.objects.get(pk=researchitem_id)
        _researchitem = m.ResearchItemSerializer(_researchitem).data
        return JsonResponse({'success':True, 'content':_researchitem}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def researchitem_answer(request, research_id, researchitem_id, answer):
    try:
        if request.user.is_authenticated:
            boo = request.user.boo
            research_id = str(research_id)
            researchitem_id = str(researchitem_id)
            # print(str(research_id) not in boo.answers, '*************')
            if research_id not in boo.answers:
                # print('*******************')
                boo.answers[research_id] = {
                    'finished': False
                }

            boo.answers[research_id][researchitem_id] = json.loads(answer)
            boo.save()
            return JsonResponse({'success':True, 'message':'answered successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while answering'}, safe=False)


# def get_isupportbrands(request):
#     _ibrands = list(set(list(m.Brand.isupportbrands)))
#     return JsonResponse({'success':True, 'ids':_ibrands}, safe=False)


def get_brand(request, brand_id):
    try:
        _brand = m.Brand.objects.get(pk=brand_id)
        _brand = m.BrandSerializer(_brand).data
        return JsonResponse({'success':True, 'content':_brand}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)



def get_istylelabels(request):
    _ilabels = list(m.Stylelabel.istylelabels)
    return JsonResponse({'success':True, 'ids':_ilabels}, safe=False)


def get_iitemlabels(request):
    _ilabels = list(m.Itemlabel.iitemlabels)
    return JsonResponse({'success':True, 'ids':_ilabels}, safe=False)


def get_stylelabel(request, label_id):
    try:
        _label = m.Stylelabel.objects.get(pk=label_id)
        _label = m.StylelabelSerializer(_label).data
        return JsonResponse({'success':True, 'content':_label}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_itemlabel(request, label_id):
    try:
        _label = m.Itemlabel.objects.get(pk=label_id)
        _label = m.ItemlabelSerializer(_label).data
        return JsonResponse({'success':True, 'content':_label}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def save_mylabels(request):
    try:
        if request.user.is_authenticated:
            _boo = request.user.boo
            _type = request.GET.get('type', None)
            _add = json.loads(request.GET.get('add', None))
            _remove = json.loads(request.GET.get('remove', None))

            getattr(_boo, _type).add(*_add)
            getattr(_boo, _type).remove(*_remove)

        return JsonResponse({'success':True, 'message':'mylabels edited successfully'}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def edit_mylabels(request):
    try:
        if request.user.is_authenticated:
            _boo = request.user.boo
            _type = request.GET.get('type', None)
            _action = request.GET.get('action', None)
            _id = request.GET.get('id', None)

            if _action == 'add':
                getattr(_boo, _type).add(int(_id))

            elif _action == 'remove':
                getattr(_boo, _type).remove(int(_id))

        return JsonResponse({'success':True, 'message':'mylabels edited successfully'}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)



def get_icoffeecoupons(request):
    _icc = list(m.Coffeecoupon.icoffeecoupons)
    return JsonResponse({'success':True, 'ids':_icc}, safe=False)


def get_coffeecoupon(request, coffeecoupon_id):
    try:
        _cc = m.Coffeecoupon.objects.get(pk=coffeecoupon_id)
        _cc = m.CoffeecouponSerializer(_cc).data
        return JsonResponse({'success':True, 'content':_cc}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)



# def buy_shoptem(request, shoptem_id):
#     try:
#         if request.user.is_authenticated:
#             request.user.shop_notify(shoptem_id)
#             return JsonResponse({'success':True, 'message':'bought and notified successfully'}, safe=False)
#
#         else:
#             return JsonResponse({'success':True, 'message':'something wrong while finalizing shopping'}, safe=False)
#
#     except:
#         return JsonResponse({'success':True, 'message':'something wrong while finalizing shopping'}, safe=False)


def get_ishoptems(request):
    _ishoptems = list(m.Shoptem.ishoptems)
    return JsonResponse({'success':True, 'ids':_ishoptems}, safe=False)


def get_shoptem(request, shoptem_id):
    try:
        _shoptem = m.Shoptem.objects.get(pk=shoptem_id)
        _shoptem = m.ShoptemSerializer(_shoptem).data
        return JsonResponse({'success':True, 'content':_shoptem}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_iraffles_my(request):
    try:
        if request.user.is_authenticated:
            _boo = request.user.boo
            _iraffles = list(m.Raffle.iraffles(_boo))
            return JsonResponse({'success':True, 'ids':_iraffles}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_iraffles(request):
    _iraffles = list(m.Raffle.iraffles())
    return JsonResponse({'success':True, 'ids':_iraffles}, safe=False)


def get_raffle(request, raffle_id):
    try:
        _raffle = m.Raffle.objects.get(pk=raffle_id)
        _raffle = m.RaffleSerializer(_raffle).data
        return JsonResponse({'success':True, 'content':_raffle}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def raffle_send_request(request, raffle_id):
    try:
        if request.user.is_authenticated:
            _raffle = m.Raffle.objects.get(pk=raffle_id)
            _raffle.send_requested = True
            _raffle.save()

            _trans = _raffle.wallet.receiver_transaction_set.filter(sender__boo=request.user.boo).last()
            m.Notihistory.add(_trans.id)
            return JsonResponse({'success':True, 'message':'raffle send requested successfully'}, safe=False)

        else:
            return JsonResponse({'success':False, 'message':'something wrong while raffle send requesting'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while raffle send requesting'}, safe=False)


def get_iflashgames(request):
    _iflashgames = list(m.Flashgame.iflashgames)
    return JsonResponse({'success':True, 'ids':_iflashgames}, safe=False)


def get_flashgame(request, flashgame_id):
    try:
        _flashgame = m.Flashgame.objects.get(pk=flashgame_id)
        _flashgame = m.FlashgameSerializer(_flashgame).data
        return JsonResponse({'success':True, 'content':_flashgame}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def flashgame_answer(request):
    try:
        if request.user.is_authenticated:
            _boo = request.user.boo
            _flashgame_id = request.GET.get('flashgame_id', None)
            _answer = json.loads(request.GET.get('answer', None))

            _flashgame = m.Flashgame.objects.get(pk=_flashgame_id)
            _mytags = _flashgame.flashgametag_set.filter(who=_boo)

            if _mytags.count() > 0:
                _mytag = _mytags[0]
                _mytag.answer = _answer
                _mytag.save()

            else:
                m.Flashgametag.objects.create(on=_flashgame, who=_boo, answer=_answer)

            return JsonResponse({'success':True, 'message':'answered successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while answering'}, safe=False)


def balancegame_stat(request):
    try:
        if request.user.is_authenticated:
            _user = request.user
            return JsonResponse({'success':True, 'stat':_user.boo.balancegame_stat, 'message': 'balancegame stat evaluated successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message': 'something wrong while evaluating balancegame stat'}, safe=False)


def balancegame_stat2(request):
    try:
        if request.user.is_authenticated:
            _user = request.user
            return JsonResponse({'success':True, 'stat':_user.boo.balancegame_stat2, 'message': 'balancegame stat evaluated successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message': 'something wrong while evaluating balancegame stat'}, safe=False)


def get_item(request, item_id):
    try:
        _item = m.Item.objects.get(pk=item_id)
        _item = m.ItemSerializer(_item).data
        return JsonResponse({'success':True, 'content':_item}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_support(request, support_id):
    try:
        _support = m.Support.objects.get(pk=support_id)
        _support = m.SupportSerializer(_support).data
        return JsonResponse({'success':True, 'content':_support}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_isupports_my(request):
    try:
        if request.user.is_authenticated:
            _boo = request.user.boo
            _isupports = list(m.Support.isupports(_boo))
            return JsonResponse({'success':True, 'ids':_isupports}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_isupports(request):
    _isupports = list(m.Support.isupports())
    return JsonResponse({'success':True, 'ids':_isupports}, safe=False)


# def get_isupports(request, brand_id):
#     _brand = m.Brand.objects.get(pk=brand_id)
#     _isupports = list(_brand.isupports)
#     return JsonResponse({'success':True, 'ids':_isupports}, safe=False)


def _pix_combinations(n):
    _ipixs = list(m.Pix.ipixs())
    comb = set()

    while len(comb) < n:
        comb.add(frozenset(random.sample(_ipixs, 2)))

    return comb


def get_ipixs_comb(request, n):
    _comb = _pix_combinations(n)
    _comb = [sorted(list(e)) for e in _comb]
    return JsonResponse({'success':True, 'ids':_comb}, safe=False)


def get_ipixs(request):
    _ipixs = list(m.Pix.ipixs())
    random.shuffle(_ipixs)
    return JsonResponse({'success':True, 'ids':_ipixs}, safe=False)


# def pixpair_exists(bgr, ipixpair):
#     return (bgr['pix_0'] == ipixpair[0]) and (bgr['pix_1'] == ipixpair[1])


# tmp = [0]
# def get_kkk():
#     tmp[0] = 1
#     return [4140, 4145]


def get_pixpair_ipixs(request):
    _user = request.user

    # st = time.time()
    # # https://stackoverflow.com/questions/1731346/how-to-get-two-random-records-with-django/6405601#6405601
    # _type = random.choice(['X', 'M', 'F', 'T'])
    # _univ = m.Pix.objects.filter(type=_type)
    # _ilast = _univ.count() - 1
    #
    # _i0 = random.randint(0, _ilast)
    # _i1 = random.randint(0, _ilast - 1)
    # if _i0 == _i1: _i1 = _ilast
    #
    # _ipixs = sorted([_univ[_i0].id, _univ[_i1].id])
    # print(_ipixs, '****************', time.time() - st)

    # st = time.time()

    if _user.is_authenticated and (_user.gender == 0):
        __type = ['X', 'M', 'T']

    else:
        __type = ['X', 'M', 'F', 'T']

    _type = random.choice(__type)
    _univ = m.Pix.objects.filter(type=_type).values_list('id', flat=True)
    _ipixs = sorted(random.sample(list(_univ), 2))

    if _user.is_authenticated:
        if _user.has_active_boo and _user.boo.balancegamerecord_set.filter(pix_0_id=_ipixs[0], pix_1_id=_ipixs[1]).exists():
            return get_pixpair_ipixs(request)

        else:
            return JsonResponse({'success':True, 'ids':_ipixs}, safe=False)

    else:
        return JsonResponse({'success':True, 'ids':_ipixs}, safe=False)



def get_tag(request, tag_id):
    try:
        _tag = m.Tag.objects.get(pk=tag_id)
        _tag = m.TagSerializer(_tag).data
        return JsonResponse({'success':True, 'content':_tag}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


univ = [
    [10, {'type':'clothing', 'category':'캐주얼상의'}],
    [10, {'type':'clothing', 'category':'팬츠'}],
    [10, {'type':'clothing', 'category':'재킷'}],
    [10, {'type':'clothing', 'category':'니트웨어'}],
    [10, {'type':'clothing', 'category':'청바지'}],
    [10, {'type':'clothing', 'category':'스커트'}],
    [10, {'type':'clothing', 'category':'셔츠'}],
    [10, {'type':'clothing', 'category':'점퍼'}],
    [10, {'type':'clothing', 'category':'코트'}],
    [9, {'type':'clothing', 'category':'드레스'}],
    [8, {'type':'clothing', 'category':'블라우스'}],
    [7, {'type':'clothing', 'category':'탑'}],
    [6, {'type':'clothing', 'category':'패딩'}],
    [3, {'type':'clothing', 'category':'베스트'}],
    [2, {'type':'clothing', 'category':'점프수트'}],
    [1, {'type':'clothing', 'category':'수영복'}],

    [7, {'type':'shoes'}],
    [7, {'type':'shoes', 'category':'운동화'}],
    [7, {'type':'shoes', 'category':'부츠/워커'}],
    [7, {'type':'shoes', 'category':'로퍼'}],
    [6, {'type':'shoes', 'category':'슬리퍼'}],
    [5, {'type':'shoes', 'category':'펌프스'}],
    [4, {'type':'shoes', 'category':'정장구두'}],
    [4, {'type':'shoes', 'category':'샌들'}],

    [5, {'type':'bags', 'category':'가방'}],
    [1, {'type':'bags', 'category':'지갑'}],

    [1, {'type':'accessories', 'category':'잡화', 'item':'선글라스'}],
    [1, {'type':'accessories', 'category':'잡화', 'item':'벨트'}],
    [1, {'type':'accessories', 'category':'잡화', 'item':'안경'}],
    [1, {'type':'accessories', 'category':'잡화', 'item':'손목시계'}],
    [1, {'type':'accessories', 'category':'잡화', 'item':'머플러'}],
    [1, {'type':'accessories', 'category':'잡화', 'item':'헤어밴드'}],
    [1, {'type':'accessories', 'category':'잡화', 'item':'스카프'}],
    [1, {'type':'accessories', 'category':'잡화', 'item':'양말'}],
    [1, {'type':'accessories', 'category':'잡화', 'item':'헤어악세서리'}],
#     {'type':'accessories', 'category':'잡화', 'item':'고글'},
#     {'type':'accessories', 'category':'잡화', 'item':'넥워머'},
#     {'type':'accessories', 'category':'잡화', 'item':'넥타이'},
#     {'type':'accessories', 'category':'잡화', 'item':'타이츠스타킹'},
#     {'type':'accessories', 'category':'잡화', 'item':'암워머'},

    [1, {'type':'jewelries'}],
    [1, {'type':'jewelries', 'category':'목걸이'}],
    [1, {'type':'jewelries', 'category':'팔찌/발찌'}],
    [1, {'type':'jewelries', 'category':'귀걸이/피어싱'}],
    [1, {'type':'jewelries', 'category':'반지'}],
#     {'type':'jewelries', 'category':'펜던트'},

    [3, {'type':'hats', 'category':'모자'}],
]

df_choice = pd.DataFrame(univ)


def __itags():
    try:
        _itags = m.Tag.objects.filter(**random.choices(df_choice[1], weights=df_choice[0])[0]).order_by('?')[:2].values_list('id', flat=True)
        return sorted(list(_itags))

    except:
        return __itags()


def get_itags(request):
    return JsonResponse({'success':True, 'ids':__itags()}, safe=False)
    # try:
    #     _itags = m.Tag.objects.filter(**random.choices(df_choice[1], weights=df_choice[0])[0]).order_by('?')[:2].values_list('id', flat=True)
    #     _itags = sorted(list(_itags))
    #     return JsonResponse({'success':True, 'ids':_itags}, safe=False)
    # except:
    #     return get_itags(request)

def get_itags_many(request, n):
    _itags_many = [__itags() for i in range(n)]
    return JsonResponse({'success':True, 'ids':_itags_many}, safe=False)


def get_random_icols(request):
    _icols = m.Collection.icols()
    random.shuffle(_icols)
    return JsonResponse({'success':True, 'ids':_icols}, safe=False)


def get_icollections(request, boo_id):
    _icols = m.Boo.objects.get(id=boo_id).icollections
    return JsonResponse({'success':True, 'ids':_icols}, safe=False)


def get_pix(request, pix_id):
    try:
        _pix = m.Pix.objects.get(pk=pix_id)
        _pix = m.PixSerializer(_pix).data
        return JsonResponse({'success':True, 'content':_pix}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def collect_pix(request, collection_id, pix_id):
    try:
        pick = m.Pick.objects.create(collection_id=collection_id, pix_id=pix_id)
        # print(collections.Counter(pick.pix.tokens.split()))

        _boo = pick.collection.owner
        _boo.coltags = collections.Counter(_boo.coltags) + collections.Counter(pick.pix.tokens.split())
        # _boo.rewarding(n_collected=1, amount_by_collect=100)
        _boo.save()
        return JsonResponse({'success':True, 'pick_id':pick.id, 'message':'pix collected successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while collecting pix'}, safe=False)


def get_ipicks(request, collection_id):
    _ipicks = m.Collection.objects.get(pk=collection_id).ipicks
    return JsonResponse({'success':True, 'ids':_ipicks}, safe=False)


def get_collection(request, collection_id):
    _col = m.Collection.objects.get(id=collection_id)
    return JsonResponse({'success':True, 'content':_col.serialized}, safe=False)


def get_collection_base(request, collection_id):
    _col = m.Collection.objects.get(id=collection_id)
    return JsonResponse({'success':True, 'content':_col.serialized_base}, safe=False)


def get_collection_ipixs(request, collection_id):
    _ipixs = m.Pix.objects.filter(pick__collection_id=collection_id)
    _ipixs = _ipixs.values_list('id', flat=True)
    return JsonResponse({'success':True, 'ids':list(_ipixs)}, safe=False)


def get_pick(request, pick_id):
    try:
        _pick = m.Pick.objects.get(pk=pick_id)
        return JsonResponse({'success':True, 'content':_pick.serialized}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def remove_picks(request, collection_id, pick_ids):
    try:
        _boo = request.user.boo
        _pids = pick_ids.split(',')
        _toks = m.Pix.objects.filter(pick__in=_pids).values_list('tokens', flat=True)
        # print(collections.Counter(' '.join(_toks).split()))
        _boo.coltags = collections.Counter(_boo.coltags) - collections.Counter(' '.join(_toks).split())
        _boo.save()

        _picks = m.Pick.objects.filter(collection_id=collection_id, id__in=_pids)
        _picks.delete()
        return JsonResponse({'success':True, 'message':'picks removed successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while removing picks'}, safe=False)

# def get_collection_seed(request, col_id):
#     try:
#         _col = m.Collection.objects.get(pk=col_id)
#         return JsonResponse({'success':True, 'content':_col.first_pick_serialized}, safe=False)
#
#     except:
#         return JsonResponse({'success':False}, safe=False)


def get_iposts(request, type):
    _iposts = m.Post.iposts(type)
    return JsonResponse({'success':True, 'idlist':list(_iposts)}, safe=False)


def get_mbti_iposts(request, type):
    _iposts = list(m.Post.mbti_iposts(type))
    # moiber.js와 sideb.js 둘다 사용하고 있어서,
    # idlist, ids 전부 보냈다
    return JsonResponse({'success':True, 'idlist':_iposts, 'ids':_iposts}, safe=False)


def get_contentwork(request, id):
    # _cwork = m.Contentwork.objects.get(agenda=agenda)
    _cwork = m.Contentwork.objects.get(id=id)
    return JsonResponse({'success':True, 'content':_cwork.serialized}, safe=False)


def get_contentwork_ipostages(request, id):
    # _ipostages = list(m.Contentwork.ipostages(agenda))
    _ipostages = list(m.Contentwork.ipostages(id))
    return JsonResponse({'success':True, 'ids':_ipostages}, safe=False)


def contentwork_resultize(request, id):
    if request.method=='POST':
        _result = request.POST.get('result', None)
        _result = json.loads(_result)

        if _result:
            # request.user.boo.contentwork_resultize(agenda, _result)
            request.user.boo.contentwork_resultize(id, _result)
            return JsonResponse({'success':True, 'result':_result, 'message':'contentwork resultized successfully'}, safe=False)

        else:
            return JsonResponse({'success':True, 'message':'something wrong while resultizing contentwork'}, safe=False)


def mbtiresult_base(request, type):
    return render(request, 'getch/mbtiresult_base.html')


def get_post(request, post_id):
    try:
        _post = m.Post.objects.get_subclass(pk=post_id)
        _post = m.PostSerializer(_post).data
        return JsonResponse({'success':True, 'content':_post}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_postage(request, postage_id):
    try:
        _postage = m.Postage.objects.get(pk=postage_id)
        _postage = m.PostageSerializer(_postage).data
        return JsonResponse({'success':True, 'content':_postage}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_iboos(request, type):
    if type == 'hot':
        # _iboos = m.Flager.objects.filter(status=m.FOLLOW).values('object_id').annotate(nfollowers=Count('object_id')).order_by('-nfollowers')[:10].values_list('object_id', flat=True)

        ago_2w = datetime.now() - timedelta(days=7)
        _iboos = m.Post.objects.filter(created_at__gte=ago_2w).values('boo').annotate(nposts=Count('boo')).order_by('-nposts')[:10].values_list('boo', flat=True)
        return JsonResponse({'success':True, 'idlist':list(_iboos)}, safe=False)

    else:
        pass


def get_ibooposts(request, boo_id, type):
    try:
        _boo = m.Boo.objects.get(pk=boo_id)
        return JsonResponse({'success':True, 'idlist':_boo.iposts(type)}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_ifollowers(request, boo_id):
    try:
        _boo = m.Boo.objects.get(pk=boo_id)
        # print('*********************', _boo.followers_id)
        return JsonResponse({'success':True, 'idlist':_boo.followers_id}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_boopost(request, post_id):
    try:
        _post = m.Post.objects.get_subclass(pk=post_id)
        # 내페이지에서 내가 작성하지 않은 포스트를 가져오는 경우가 있어서, PostSerializer로 바꿨다
        # 2020.12.07
        _post = m.PostSerializer(_post).data
        # _post = m.BoopostSerializer(_post).data
        return JsonResponse({'success':True, 'content':_post}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_icomments(request, post_id):
    try:
        _icomments = m.Comment.objects.filter(post_id=post_id, boo__isnull=False).values_list('id', flat=True)
        return JsonResponse({'success':True, 'idlist':list(_icomments)}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_comment(request, comment_id):
    try:
        _comment = m.Comment.objects.get(pk=comment_id)
        _comment = m.CommentSerializer(_comment).data
        return JsonResponse({'success':True, 'content':_comment}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_ivoters(request, post_id, act):
    try:
        _ivoters = m.Flager.objects.filter(object_id=post_id, status=act).values_list('user_id', flat=True)
        return JsonResponse({'success':True, 'idlist':list(_ivoters)}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_baseboo(request, boo_id):
    try:
        _baseboo = m.Boo.objects.get(pk=boo_id)

        if request.user.is_authenticated and request.user.boo_set.filter(id=boo_id).exists():
            _baseboo = m.BooSerializer(_baseboo).data

        else:
            _baseboo = m.BasebooSerializer(_baseboo).data

        return JsonResponse({'success':True, 'content':_baseboo}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def other_boos(request):
    return JsonResponse({'success':True, 'other_boos':request.user.other_boos}, safe=False)


def other_boos2(request):
    return JsonResponse({'success':True, 'other_boos':request.user.other_boos2}, safe=False)


def _labels_update(boo, labels):
    for k, v in labels.items():
        for _k, _v in v.items():
            if _k=='add':
                getattr(boo, k).add(*_v)
            if _k=='remove':
                getattr(boo, k).remove(*_v)

def boo_save(request):
    if request.method=='POST':
        print(request.POST, request.FILES)
        _on_creating = request.POST.get('on_creating', None)
        _labels = request.POST.get('labels', None)
        _boo_text = request.POST.get('boo_text', None)
        _boo_nick = request.POST.get('boo_nick', None)
        _profilepix = request.FILES.get('profilepix', None)

        try:
            # _on_creating이 있다면 그건 사실 문자열 'true' 이다
            # 그래도 if _on_creating 에서 걸러지기에, json.loads 처리를 안했다
            if _on_creating:
                boo = m.Boo.objects.create(user=request.user)
            else:
                boo = request.user.boo

            if _labels:
                _labels_update(boo, json.loads(_labels))
            # print(_boo_text, '***********')
            if _boo_text or _boo_text=='':
                # print('###########')
                boo.text = _boo_text
                boo.save()

            if _boo_nick:
                boo.nick = _boo_nick
                boo.save()

            if _profilepix:
                profile = boo.profile
                profile.pix = _profilepix
                profile.save()

            if _on_creating:
                request.user.set_boo(boo.id)
                return JsonResponse({'success':True, 'boo_id':boo.id, 'message':'boo created successfully'}, safe=False)

            else:
                return JsonResponse({'success':True, 'message':'boo updated successfully'}, safe=False)

        except:
            return JsonResponse({'success':False, 'message':'something wrong while boo saving'}, safe=False)


def link_add(request):
    try:
        _url = request.POST.get('url', None)
        _link = m.Link.objects.create(user=request.user, url=_url)
        return JsonResponse({'success':True, 'link_id':_link.id, 'message':'link added successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while link adding'}, safe=False)


def link_edit(request):
    try:
        _url = request.POST.get('url', None)
        _id = request.POST.get('id', None)
        _link = m.Link.objects.get(id=_id)
        _link.url = _url
        _link.save()
        return JsonResponse({'success':True, 'message':'link edited successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while link editing'}, safe=False)


def link_delete(request, link_id):
    try:
        _link = m.Link.objects.get(id=link_id)
        _link.delete()
        return JsonResponse({'success':True, 'message':'link deleted successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while link deleting'}, safe=False)



def transact(request):
    try:
        if request.user.is_authenticated:
            _receiver_id = request.GET.get('receiver_id', None)
            _type = request.GET.get('type', None)
            _amount = int(request.GET.get('amount', 0))

            if _type == 'support':
                _sender = request.user.boo.wallet
                _receiver = m.Support.objects.get(pk=_receiver_id).wallet

            elif _type == 'raffle':
                _sender = request.user.boo.wallet
                _receiver = m.Raffle.objects.get(pk=_receiver_id).wallet

            elif _type == 'shoptem':
                _sender = request.user.boo.wallet
                _receiver = m.Shoptem.objects.get(pk=_receiver_id).wallet
                # _receiver = m.Boo.objects.get(pk=m.MOIBER_BOO).wallet

            elif _type == 'coffeecoupon':
                _sender = request.user.boo.wallet
                _receiver = m.Coffeecoupon.objects.get(pk=_receiver_id).wallet

            elif _receiver_id is None:
                _sender = m.Boo.objects.get(pk=m.MOIBER_BOO).wallet
                _receiver = request.user.boo.wallet

            _sender.send(to=_receiver, type=_type, amount=_amount)
            return JsonResponse({'success':True, 'message':'transacted successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while transaction'}, safe=False)



# def wallet_write(request):
#     try:
#         _obj = request.GET.get('obj', None)
#         _obj_id = request.GET.get('obj_id', None)
#         _type = request.GET.get('type', None)
#         _amount = int(request.GET.get('amount', 0))
#
#         if _obj == 'support':
#             obj = m.Support.objects.get(pk=_obj_id)
#
#         elif _obj == 'raffle':
#             obj = m.Raffle.objects.get(pk=_obj_id)
#
#         elif _obj is None:
#             obj = request.user.boo
#
#         obj.wallet.write(type=_type, amount=_amount)
#         return JsonResponse({'success':True, 'message':'transacted successfully'}, safe=False)
#
#     except:
#         return JsonResponse({'success':False, 'message':'something wrong while transaction'}, safe=False)



def settle(request):
    # if request.user.is_authenticated:
    try:
        _boo = request.user.boo
        n_collected = int(request.GET.get('n_collected', 0))
        n_voted = int(request.GET.get('n_voted', 0))
        collect_reward = int(request.GET.get('collect_reward', 0))
        vote_reward = int(request.GET.get('vote_reward', 0))
        checkin_reward = int(request.GET.get('checkin_reward', 0))
        bonus_reward = int(request.GET.get('bonus_reward', 0))
        _boo.settle(n_collected=n_collected, n_voted=n_voted, collect_reward=collect_reward, vote_reward=vote_reward, checkin_reward=checkin_reward, bonus_reward=bonus_reward)
        return JsonResponse({'success':True, 'message':'settled successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while settle'}, safe=False)



def balancegame_vote(request):
    try:
        itag_pos = int(request.GET.get('itag_pos', None))
        itag_neg = int(request.GET.get('itag_neg', None))
        toggletype = request.GET.get('type', None)

        if request.user.is_authenticated and itag_pos and itag_neg and toggletype:
            _boo = request.user.boo

            if toggletype == 'clear':
                try:
                    m.BalancegameRecord.objects.filter(who=_boo, tag_pos_id=itag_pos, tag_neg_id=itag_neg).last().delete()
                except:
                    pass

            elif toggletype == 'change':
                try:
                    _bgr = m.BalancegameRecord.objects.filter(who=_boo, tag_pos_id=itag_neg, tag_neg_id=itag_pos).last()
                    _bgr.tag_pos_id = itag_pos
                    _bgr.tag_neg_id = itag_neg
                    _bgr.save()
                except:
                    pass

            else: # toggletype=='new'
                m.BalancegameRecord.objects.create(who=_boo, tag_pos_id=itag_pos, tag_neg_id=itag_neg)

            # _boo.save()
            return JsonResponse({'success':True, 'message':'balancegame voted successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while balancegame voting'}, safe=False)



def stylevote(request):
    try:
        ipix_pos = int(request.GET.get('ipix_pos', None))
        ipix_neg = int(request.GET.get('ipix_neg', None))
        toggletype = request.GET.get('type', None)

        if request.user.is_authenticated and ipix_pos and ipix_neg and toggletype:
            _pix_pos = m.Pix.objects.get(pk=ipix_pos)
            _pix_neg = m.Pix.objects.get(pk=ipix_neg)
            _tags_pos = collections.Counter(_pix_pos.tokens.split())
            _tags_neg = collections.Counter(_pix_neg.tokens.split())
            _boo = request.user.boo

            _pix_0 = min(ipix_pos, ipix_neg)
            _pix_1 = max(ipix_pos, ipix_neg)
            _chosen = 0 if (_pix_0 == ipix_pos) else 1

            if toggletype == 'clear':
                _boo.postags = collections.Counter(_boo.postags) - _tags_neg
                _boo.negtags = collections.Counter(_boo.negtags) - _tags_pos

                try:
                    m.BalancegameRecord.objects.filter(who=_boo, pix_0_id=_pix_0, pix_1_id=_pix_1).delete()
                except:
                    pass

            elif toggletype == 'change':
                _boo.postags = collections.Counter(_boo.postags) - _tags_neg + _tags_pos
                _boo.negtags = collections.Counter(_boo.negtags) - _tags_pos + _tags_neg

                try:
                    _bgr = m.BalancegameRecord.objects.filter(who=_boo, pix_0_id=_pix_0, pix_1_id=_pix_1)[0]
                    _bgr.chosen = _chosen
                    _bgr.save()
                except:
                    pass

            else: # toggletype=='new'
                print(_boo, _pix_0, _pix_1, _chosen)
                _boo.postags = collections.Counter(_boo.postags) + _tags_pos
                _boo.negtags = collections.Counter(_boo.negtags) + _tags_neg
                m.BalancegameRecord.objects.create(who=_boo, pix_0_id=_pix_0, pix_1_id=_pix_1, chosen=_chosen)

            # _boo.rewarding(n_voted=1, amount_by_vote=10)
            _boo.save()
            return JsonResponse({'success':True, 'message':'tagged successfully'}, safe=False)
            # return JsonResponse({'success':True, 'message':'tagged successfully', 'styleprofile':_boo.styleprofile}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while tagging'}, safe=False)



def contentvote(request, postage_id):
    action = request.GET.get('action', None)

    if action:
        postage = m.Postage.objects.get(pk=postage_id)

        if request.user.is_authenticated:
            postage.contentvote(int(action), request.user.boo)

        else:
            postage.contentvote(int(action), m.Boo.guestboo, note=request.session.session_key)

        return JsonResponse({'success':True, 'action':action}, safe=False)

    else:
        return JsonResponse({'success':False}, safe=False)



def vote(request, post_id):
    action = request.GET.get('action', None)
    # fit = session.fit #request.user.boo.fit
    # fit = request.user.boo.fit

    if action:
        post = m.Post.objects.get(pk=post_id)

        if request.user.is_authenticated:
            # fit = request.user.boo.fit
            post.vote(int(action), request.user.boo)

        else:
            # fit = []
            post.vote(int(action), m.Boo.guestboo, note=request.session.session_key)

        # post.vote(int(action), request.user.boo)
        # session.vote(post_id, action)
        # return JsonResponse({'success':True, 'action':action, 'fit':fit}, safe=False)
        return JsonResponse({'success':True, 'action':action}, safe=False)

    else:
        return JsonResponse({'success':False}, safe=False)


def create_collection(request, name):
    try:
        col = m.Collection.objects.create(owner=request.user.boo, name=name)
        return JsonResponse({'success':True, 'collection_id':col.id, 'message':'collection created successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while creating collection'}, safe=False)


def set_boo(request, boo_id):
    try:
        request.user.set_boo(boo_id)
        return JsonResponse({'success':True}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def follow(request, boo_id):
    try:
        request.user.boo.follow(boo_id)
        return JsonResponse({'success':True}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def unfollow(request, boo_id):
    try:
        request.user.boo.unfollow(boo_id)
        return JsonResponse({'success':True}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def like_comment(request, comment_id):
    try:
        comment = m.Comment.objects.get(pk=comment_id)

        if request.user.is_authenticated:
            comment.like(request.user.boo)

        else:
            comment.like(m.Boo.guestboo, note=request.session.session_key)

        return JsonResponse({'success':True, 'message':'Comment liked successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'Something wrong when liking comment'}, safe=False)


def delike_comment(request, comment_id):
    try:
        comment = m.Comment.objects.get(pk=comment_id)

        if request.user.is_authenticated:
            comment.delike(request.user.boo)

        else:
            comment.delike(m.Boo.guestboo, note=request.session.session_key)

        return JsonResponse({'success':True, 'message':'Comment deliked successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'Something wrong when deliking comment'}, safe=False)


def boo_profilepix(request, boo_id):
    _boo = m.Boo.objects.get(pk=boo_id)
    return JsonResponse({'success':True, 'pix':_boo.profile.pix.url}, safe=False)


def post_delete(request, post_id):
    try:
        post = m.Post.objects.get_subclass(pk=post_id)
        post.delete()
        return JsonResponse({'success':True, 'message':'post deleted successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while deleting post'}, safe=False)


def voters(request, post_id):
    try:
        post = m.Post.objects.get(pk=post_id)
        return JsonResponse({'success':True, 'voters':post.voters}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def profile_delete(request):
    try:
        request.user.delete_boo()
        return JsonResponse({'success':True, 'message':'boo deleted successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while deleting boo'}, safe=False)



def comment_save(request):
    if request.method == 'POST':
        print(request.POST, request.FILES)
        post_id = request.POST.get('post_id', None)
        text = request.POST.get('text', None)
        id = request.POST.get('id', None)
        mention_id = request.POST.get('mention_id', None)
        attached = request.FILES.get('attached', None)
        # return

        # if text and post_id:
        if post_id:
            if id:
                comment = m.Comment.objects.get(pk=id)

                if text:
                    comment.text = text

                if mention_id:
                    comment.mention = m.Boo.objects.get(id=mention_id)

                comment.save()

            else:
                if request.user.is_authenticated:
                    comment = m.Comment(boo=request.user.boo, post_id=post_id)
                else:
                    comment = m.Comment(boo=m.Boo.guestboo, post_id=post_id)

                if text:
                    comment.text = text

                if mention_id:
                    comment.mention = m.Boo.objects.get(id=mention_id)
                    # comment = m.Comment.objects.create(boo=request.user.boo, post_id=post_id, text=text, mention_id=mention_id)

                # else:
                #     comment = m.Comment.objects.create(boo=request.user.boo, post_id=post_id, text=text)

                comment.save()

                if attached:
                    commentpix = m.Commentpix.objects.create(comment_id=comment.id, img=attached)


            return JsonResponse({'success':True, 'message':'successfully commented', 'comment_id':comment.id}, safe=False)

        else:
            return JsonResponse({'success':False, 'message':'something wrong on commenting'}, safe=False)



def post_save(request):
    if request.method == 'POST':
        print(request.POST, request.FILES)

        post_id = request.POST.get('post_id', None)
        post_type = request.POST.get('type', None)
        text = request.POST.get('text', None)
        keys = request.POST.get('keys', None)
        pix = request.FILES.get('pix', None)
        pix_a = request.FILES.get('pix_a', None)
        pix_b = request.FILES.get('pix_b', None)
        pixlabel_a = request.POST.get('pixlabel_a', None)
        pixlabel_b = request.POST.get('pixlabel_b', None)

        if post_id:
            mode = 'edited'
            post = m.Post.objects.get_subclass(pk=post_id)

        else:
            mode = 'created'
            postmodel = apps.get_model(app_label='getch', model_name=post_type)
            post = postmodel(boo=request.user.boo)

        if text:        post.text = text
        if keys:        post.keys = keys
        if pix:         post.pix = pix
        if pix_a:       post.pix_a = pix_a
        if pix_b:       post.pix_b = pix_b
        if pixlabel_a:  post.pixlabel_a = pixlabel_a
        if pixlabel_b:  post.pixlabel_b = pixlabel_b
        post.save()

        if mode == 'edited':
            js = {'success':True, 'mode':mode}

        elif mode == 'created':
            # _post = m.PostSerializer(post).data
            js = {'success':True, 'mode':mode, 'post_id':post.id}
            # js = {'success':True, 'mode':mode, 'post':_post}
            # post_created = render_to_string('getch/post.html', {'post':post, 'type':post_type})
            # js = {'success':True, 'mode':mode, 'post_id':post.id, 'post_created':post_created}

        return JsonResponse(js, safe=False)


def network(request, boo_id):
    boo = m.Boo.objects.get(pk=boo_id)
    return JsonResponse({'success':True, 'network':boo.network}, safe=False)



def search(request, keywords):
    n = 20
    # q = request.GET.get('q', None)

    try:
        vector = SearchVector('text', 'boo__nick', 'boo__text')
        query = SearchQuery(keywords)
        excl = Q(boo_id=m.BOO_DELETED) | Q(boo__hidden=True)
        _searched = m.Post.objects.exclude(excl).annotate(rank=SearchRank(vector, query)).order_by('-rank')[:n]
        # _searched = m.Post.objects.exclude(boo_id=m.BOO_DELETED).annotate(rank=SearchRank(vector, query)).order_by('-rank')[:n]
        # print(_searched)
        _searched = _searched.values_list('id', flat=True)
        return JsonResponse({'success':True, 'idlist':list(_searched), 'message':'searched successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while searching'}, safe=False)


def search_by_pix(request, pix_id):
    # n = 50

    try:
        pix = m.Pix.objects.get(pk=pix_id)

        # _searched = m.Pix.objects.annotate(similarity=TrigramSimilarity('tokens', '나이키')).order_by('-similarity')
        # print(_searched, '**********************')
        st = datetime.now()
        vector = SearchVector('tokens')
        query = SearchQuery(pix.tokens)
        _searched = m.Pix.objects.exclude(id=pix.id).annotate(rank=SearchRank(vector, query)).exclude(rank=0).order_by('-rank')
        # print(_searched.values('id','rank'))
        _searched = _searched.values_list('id', flat=True)
        print(datetime.now()-st, '*******************************')
        return JsonResponse({'success':True, 'ids':list(_searched), 'message':'searched successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while searching'}, safe=False)


def search_by_collection(request, collection_id):
    # n = 50

    try:
        pixs = m.Pix.objects.filter(pick__collection_id=collection_id)
        tokens = ' '.join(pixs.values_list('tokens', flat=True))
        tokens = ' '.join(dict(collections.Counter(tokens.split()).most_common(30)).keys())
        # pixs = m.Pix.objects.filter(pick__collection_id=collection_id).order_by('?')[:5]
        # tokens = ' '.join(pixs.values_list('tokens', flat=True))
        # print(tokens)
        # return

        vector = SearchVector('tokens')
        query = SearchQuery(tokens)
        _searched = m.Pix.objects.exclude(pick__collection_id=collection_id).annotate(rank=SearchRank(vector, query)).exclude(rank=0).order_by('-rank')
        # print(_searched.values('id','rank'))
        _searched = _searched.values_list('id', flat=True)

        _append = list(m.Pix.ipixs())
        random.shuffle(_append)
        _searched = list(_searched) + _append
        return JsonResponse({'success':True, 'ids':_searched, 'message':'searched successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while searching'}, safe=False)


def search_by_keyword(request, keyword):
    try:
        _keyword = keyword
        vector = SearchVector('tokens', 'pick__collection__name', 'owner__nick')
        query = SearchQuery(_keyword)

        _searched = m.Pix.objects.annotate(rank=SearchRank(vector, query)).exclude(rank=0).order_by('-rank')#[:n]
        # print(_searched.values('id','rank'))
        _searched = _searched.values_list('id', flat=True)
        # print(_searched.values('id').distinct())

        _append = list(m.Pix.ipixs())
        random.shuffle(_append)
        _searched = list(_searched) + _append
        # _searched = _searched.union(_append)

        return JsonResponse({'success':True, 'ids':_searched, 'message':'searched successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while searching'}, safe=False)


class Logout(LogoutView):
    def logout(self):
        super().logout()
        # print('---------------------------------------------', session)

# class Login(LoginView):
#     def login(self):
#         super().login()
#         print(session)
