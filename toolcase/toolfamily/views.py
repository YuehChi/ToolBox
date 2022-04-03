from asyncio.windows_events import NULL
import django, json, smtplib
from django.dispatch import receiver
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.db.models import Q
from .models import *

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.backends import ModelBackend

import base64
from itsdangerous import URLSafeTimedSerializer as utsr
from django.conf import settings as django_settings
from django.core.mail import send_mail


@login_required
def index(request):
   
    # number of visits to this view
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # return user name
    if 'user' in request.session:
        user_name = UserDetail.objects.get(Q(django_user=request.session['user']))

    return render(
        request,
        'index.html',
        context={'num_visits': num_visits,
                 'user_name': user_name},
    )

#########################################
#                 TOOLS                 #
#########################################
# ---------------def Token-----------------
class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.b64encode(security_key.encode('UTF-8'))
    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)
    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)
    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)
token_confirm = Token(django_settings.SECRET_KEY)

# ----------------def ajax response----------------
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'




#########################################
#              AUTH MODULE              #
#########################################

# ----------------login------------------
def login(request):
    error = False  # wrong account or pwd 
    suspended = False  # is active or not
    valid = False  # email is verified or not
    alert = False  # show message for register

    # show message for register
    if 'messages' in request.session:
        alert = True
        sign_up_message = json.dumps(request.session['messages'])
        del request.session['messages']

    # already login
    if request.user.is_authenticated:
        return HttpResponseRedirect('home/')

    if request.method == 'POST':
        account = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=account, password=password)

        if user is not None:
            userDetail = UserDetail.objects.get(Q(account_mail=account))

            # check email is verified or not
            isValid = userDetail.verification
            if not isValid:
                valid = True
                return render(request, 'login.html', locals())

            # check suspended or not
            isActive = userDetail.isActive
            if not isActive:
                suspended = True
                return render(request, 'login.html', locals())

            # login and create session
            auth.login(request, user)
            request.session['user'] = user.pk

            return HttpResponseRedirect('home/')

        # send error message
        elif account != "":
            error = True
        return render(request, 'login.html', locals())

    return render(request, 'login.html', locals())

# -----------customize authentication-----------
class CustomizeUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserDetail.objects.get(Q(account_mail=username))
        except UserDetail.DoesNotExist as e:
            return None
        if check_password(password, user.django_user.password):
            return user.django_user

# ----------------logout------------------
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

# ----------------register------------------
# @csrf_exempt
def register(request):
    if request.method == 'POST':
        email_send_error = False  # fail to send mail

        username = request.POST.get('username')
        account = request.POST.get('account')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        # send verification url to user email
        token = token_confirm.generate_validate_token(username)
        url = 'http://127.0.0.1:8000/toolfamily/activate/' + token

        title = "NTU TOOLBOX 註冊驗證"
        msg = "歡迎加入 NTU TOOLBOX! 請點選下方連結完成註冊驗證。\n" + url
        email_from = django_settings.DEFAULT_FROM_EMAIL
        receiver = [account]

        try:
            send_mail(title, msg, email_from, receiver, fail_silently=False)
        except:
            email_send_error = True
            return render(request, 'register.html', locals())

        # insert user detail into User
        user = User.objects.create_user(username=username, password=password, email=account, is_active=False)
        user.save()

        # insert user detail into UserDetail
        userDetail = UserDetail.objects.create(name=username, django_user=user, account_mail=account, salt=password)
        userDetail.save()

        request.session['messages'] = "請查看信箱點擊連結以完成註冊驗證。\n連結有效期為1個小時。"
        return HttpResponseRedirect('/')

    # check the email is used or not
    if is_ajax(request=request):
        email_used_error = False
        account = request.POST.get("account")

        try:
            user = UserDetail.objects.get(Q(account_mail=account))
            email_used_error = True
        except:
            email_used_error = False

        return HttpResponse(email_used_error)

    return render(request, 'register.html', locals())

# ------------email verification-------------
def active(request, token):
    # timeout
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        user = User.objects.get(Q(username=username))
        user.delete()
        request.session['messages'] = "對不起，驗證連結已過期。\n請重新註冊。"
        return HttpResponseRedirect('/')

    # success
    try:
        user = User.objects.get(Q(username=username))
        user.is_active = True
        user.save()

        userDetail = UserDetail.objects.get(Q(django_user=user))
        userDetail.verification = True
        userDetail.save()

        request.session['messages'] = "驗證成功！\n登入並開始使用 NTU TOOLBOX！"
        return HttpResponseRedirect('/')
     
    except User.DoesNotExist: # user doesn't exist
        request.session['messages'] = "對不起，您所驗證的帳號不存在。\n請重新註冊。"
        return HttpResponseRedirect('/')

# --------------forget password----------------
def forget(request):
    if request.method == 'POST':
        error = False  # account doesn't exist
        account = request.POST.get('account')
        print(account)
        try:
            user = UserDetail.objects.get(Q(account_mail=account))
            print(user)
            username = user.name

            # send reset-pwd url to user email
            token = token_confirm.generate_validate_token(username)
            url = 'http://127.0.0.1:8000/toolfamily/reset/' + token

            title = "NTU TOOLBOX 重新設定密碼"
            msg = "請點選下方連結重新設定密碼。\n" + url
            email_from = django_settings.DEFAULT_FROM_EMAIL
            receiver = [account]
            send_mail(title, msg, email_from, receiver, fail_silently=False)

            request.session['messages'] = "請查看信箱點擊連結並重新設定密碼。\n連結有效期為1個小時。"
            return HttpResponseRedirect('/')

        except:
            error = True
            return render(request, 'forget_pwd.html', locals())

    return render(request, 'forget_pwd.html', locals())

# --------------reset password----------------
def reset(request, token):
    # timeout
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        user = User.objects.get(Q(username=username))
        user.delete()
        request.session['messages'] = "對不起，重新設定密碼連結已過期。"
        return HttpResponseRedirect('/')

    # reset password
    if request.method == 'POST':
        error = False
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        # check password is equal to confirm pwd or not
        if password != confirm:
            error = True
            return render(request, 'reset_pwd.html', locals())

        # update datebase
        user = User.objects.get(Q(username=username))
        user.password = make_password(password)
        user.save()

        userDetail = UserDetail.objects.get(Q(django_user=user))
        userDetail.salt = user.password
        userDetail.save()

        request.session['messages'] = "密碼更改成功！"
        return HttpResponseRedirect('/')

    return render(request, 'reset_pwd.html', locals())