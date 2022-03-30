from asyncio.windows_events import NULL
import django
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from .models import *


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
#              AUTH MODULE              #
#########################################

# ----------------login------------------
def login(request):
    error = False  # wrong account or pwd 
    suspended = False  # is active or not

    # already login
    if request.user.is_authenticated:
        return HttpResponseRedirect('home/')

    account = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=account, password=password)

    if user is not None:
        auth.login(request, user)

        # check suspended or not
        userDetail = UserDetail.objects.get(Q(account_mail=account))
        isActive = userDetail.isActive
        if not isActive:
            suspended = True
            return render(request, 'login.html', locals())

        # create session
        request.session['user'] = user.pk

        return HttpResponseRedirect('home/')

    # send error message
    elif account != "":
        error = True
    return render(request, 'login.html', locals())

# -----------customize authentication-----------
class CustomizeUserBackend(auth.backends.ModelBackend):
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
def register(request):
    if request.method == 'POST':
        pwd_error = False  # password is not equal to confirm
        email_error = False  # email doesn't exist

        username = request.POST.get('username')
        account = request.POST.get('account')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        # 帳號已經存在


        # 帳號格式不對


        # check password is equal to confirm pwd or not
        if password != confirm:
            pwd_error = True
            return render(request, 'register.html', locals())

        # insert user detail into User
        user = User.objects.create_user(username=username, password=password, email=account)
        user.save()

        # insert user detail into UserDetail
        userDetail = UserDetail.objects.create(name=username,
                                               django_user=user,
                                               account_mail=account,
                                               salt=password)
        userDetail.save()

        # 寄送密碼驗證信

        return HttpResponseRedirect('/')

    return render(request, 'register.html', locals())