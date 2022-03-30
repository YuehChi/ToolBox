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
        return HttpResponseRedirect('/toolfamily/home/')

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
        
        return HttpResponseRedirect('/toolfamily/home/')

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
