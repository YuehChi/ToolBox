from calendar import c
from datetime import timedelta
import os, django, json, smtplib, base64, imaplib, time
from email.mime.text import MIMEText
from urllib import request
from site import USER_SITE
import re
from .models import *
from .forms import *

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q, F
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as django_settings
from django.core.mail import send_mail

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.backends import ModelBackend

from itsdangerous import URLSafeTimedSerializer as utsr

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



# ---------check timeout---------
def timeout(request):
    user = request.user.user_detail
    all_publish = Case.objects.filter(publisher=user)  # all cases the user publish
    all_case = Case.objects.all()  # all cases
    all_commission = CommissionRecord.objects.filter(Q(commissioned_user=user) | Q(case__in=all_publish))  # all commission the user own and take
    finish = Status.objects.get(Q(status_id=3))
    close = Status.objects.get(Q(status_id=4))

    # finish case if all of toolmen are done
    for case in all_publish:
        if case.case_status.status_id in [1, 2]:
            commission = CommissionRecord.objects.filter(case=case)
            cnt = 0
            for data in commission:
                if data.user_status.status_id == 3:
                    cnt += 1
            if cnt >= case.num:
                case.case_status = finish
                case.save()

                msg = f"案件編號#{case.case_id} {case.title}，所有工具人都已完成委託，案件完成！"
                notice = Notice.objects.create(user=user, message=msg)
                notice.save()


    # case timeout
    for case in all_case:
        if case.case_status.status_id in [1, 2] and datetime.datetime.now().astimezone() > case.ended_datetime:
            willing = CaseWillingness.objects.filter(apply_case=case)
            commission = CommissionRecord.objects.filter(case=case)
            
            # cancel all willingness
            for data in willing:
                data.delete()
                msg = f"案件編號#{case.case_id} {case.title} 已經到期，系統自動取消報名。"
                notice = Notice.objects.create(user=data.willing_user, message=msg)
                notice.save()

            for data in commission:
                # change conducting and applying for finish -> to finish status
                if data.user_status.status_id in [2, 7]:
                    data.user_status.status_id = finish
                    data.doublecheck_datetime = datetime.datetime.now()
                    data.save()
                    
                    msg = f"案件編號#{case.case_id} {case.title} 已經到期，系統自動完成委託。"
                    notice = Notice.objects.create(user=data.commissioned_user, message=msg)
                    notice.save()

                # change applying for publisher sending delete -> to close
                elif data.user_status.status_id == 5:
                    data.user_status.status_id = close
                    data.doublecheck_datetime = datetime.datetime.now()
                    data.save()
                    
                    msg = f"案件編號#{case.case_id} {case.title} 已經到期，系統自動解除委託。"
                    notice = Notice.objects.create(user=data.case.publisher, message=msg)
                    notice.save()

                # change applying for toolman sending delete -> to close
                elif data.user_status.status_id == 6:
                    data.user_status.status_id = close
                    data.doublecheck_datetime = datetime.datetime.now()
                    data.save()
                    
                    msg = f"案件編號#{case.case_id} {case.title} 已經到期，系統自動解除委託。"
                    notice = Notice.objects.create(user=data.commissioned_user, message=msg)
                    notice.save()

            # update case status
            case.case_status = finish
            case.save()

            msg = f"案件編號#{case.case_id} {case.title} 已經到期，系統自動完成案件。"
            notice = Notice.objects.create(user=case.publisher, message=msg)
            notice.save()

    # apply timeout
    for data in all_commission:
        if data.finish_datetime != None:
            delta = datetime.datetime.now().astimezone() - data.finish_datetime
            if  delta.seconds > 259200:
                
                # publisher apply for delete, user=publisher
                if data.user_status.status_id == 5:
                    data.user_status = close
                    data.doublecheck_datetime = datetime.datetime.now()
                    data.save()

                    # user = publisher
                    msg = f"案件編號#{data.case.case_id} {data.case.title}，\
                            委託人 {data.case.publisher.nickname} 發起解除請求，\
                            工具人 {data.commissioned_user.nickname} 未於三日內確認，\
                            系統自動解除委託。"

                    # user = toolman
                    msg = f"案件編號#{data.case.case_id} {data.case.title}，\
                            委託人 {data.commissioned_user.nickname} 發起解除請求，\
                            工具人 {data.case.publisher.nickname} 未於三日內確認，\
                            系統自動解除委託。"

                    notice = Notice.objects.create(user=data.case.publisher, message=msg)
                    notice.save()
                    notice = Notice.objects.create(user=data.commissioned_user, message=msg)
                    notice.save()

                # toolman apply for delete
                elif data.user_status.status_id == 6:
                    data.user_status = close
                    data.doublecheck_datetime = datetime.datetime.now()
                    data.save()

                    # user = publisher
                    msg = f"案件編號#{data.case.case_id} {data.case.title}，\
                            工具人 {data.commissioned_user.nickname} 發起解除請求，\
                            委託人 {data.case.publisher.nickname} 未於三日內確認，\
                            系統自動解除委託。"

                    # user = toolman
                    msg = f"案件編號#{data.case.case_id} {data.case.title}，\
                            工具人 {data.case.publisher.nickname} 發起解除請求，\
                            委託人 {data.commissioned_user.nickname} 未於三日內確認，\
                            系統自動解除委託。"

                    notice = Notice.objects.create(user=data.case.publisher, message=msg)
                    notice.save()
                    notice = Notice.objects.create(user=data.commissioned_user, message=msg)
                    notice.save()

                # toolman apply finish
                elif data.user_status.status_id == 7:
                    data.user_status = finish
                    data.doublecheck_datetime = datetime.datetime.now()
                    data.save()

                    # user = publisher
                    msg = f"案件編號#{data.case.case_id} {data.case.title}，\
                            工具人 {data.commissioned_user.nickname} 發起完成請求，\
                            委託人 {data.case.publisher.nickname} 未於三日內確認，\
                            系統自動完成委託。"

                    # user = toolman
                    msg = f"案件編號#{data.case.case_id} {data.case.title}，\
                            工具人 {data.case.publisher.nickname} 發起完成請求，\
                            委託人 {data.commissioned_user.nickname} 未於三日內確認，\
                            系統自動完成委託。"

                    notice = Notice.objects.create(user=data.case.publisher, message=msg)
                    notice.save()
                    notice = Notice.objects.create(user=data.commissioned_user, message=msg)
                    notice.save()

    notice = Notice.objects.filter(Q(user=user)).order_by('-created_datetime')[:10]
    return notice



#####################################
#            HOME PAGE              #
#####################################
@login_required
def index(request):
    user = get_object_or_404(  # 找出這個 user; 找不到則回傳 404 error
        UserDetail,
        django_user=request.user,
        isActive=True)  # 若是被停權的 user，一樣 404

    list_case = Case.objects.filter(shown_public=True)
    case_fields = Case_Field.objects.all()
    case_types = Case_Type.objects.all()
    case_photo = CasePhoto.objects.all()

    notice = timeout(request)
    
    return render(request, 'index.html', locals())



#####################################
#           CASE MODULE             #
#####################################

#-------------新增CASE---------------
@login_required
def case_new(request):
    user = get_object_or_404(  # 找出這個 user; 找不到則回傳 404 error
        UserDetail,
        django_user=request.user,
        isActive=True)  # 若是被停權的 user，一樣 404

    if request.method == "POST" :

        #委託人-外部鍵
        user_id = request.user.user_detail.user_id
        publisher = UserDetail.objects.get(user_id = user_id)

        #狀態-外部鍵
        case_status = Status.objects.get(status_id = "1")

        # 委託資訊
        title = request.POST.get('title')
        description = request.POST.get('description')
        reward = request.POST.get('reward')
        location = request.POST.get('location')
        constraint = request.POST.get('constraint')

        # 時間
        started_datetime = request.POST.get('started_datetime')  # 任務開始時間（預設為空）
        ended_datetime = request.POST.get('ended_datetime')

        # 新增 人數 、工作方式

        num = request.POST.get('num')
        work = request.POST.get('work')

        case = Case(title = title ,publisher = publisher, description = description , reward = reward, location = location ,
        constraint = constraint, started_datetime = started_datetime , ended_datetime = ended_datetime,case_status =case_status,
        num = num , work = work)
        case.save()


        # 外部鍵 case (抓最新一筆關聯)
        case = Case.objects.first()

        # 照片

        image = request.FILES.getlist('photo_image')
        for f in image:
            file = CasePhoto(image=f, case = case)
            file.save()


        # 類型
        type_temp = request.POST.getlist('case_type')
        for i in range(len(type_temp)):
            type = Type.objects.get(type_id = type_temp[i])
            case_type = Case_Type(case_type = type, case = case )
            case_type.save()

        # 領域
        field_temp = request.POST.getlist('case_field')
        for i in range(len(field_temp)):
            field = Field.objects.get(field_id = field_temp[i])
            case_field = Case_Field(case_field = field ,case = case)
            case_field.save()


        pk_key = case.case_id

        list_case = Case.objects.filter(Q(case_id=pk_key) & Q(shown_public=True))
        case_fields = Case_Field.objects.filter(case = pk_key)
        case_types = Case_Type.objects.filter(case = pk_key)
        case_photo = CasePhoto.objects.filter(case = pk_key)

        return redirect('case-profile',case_id = pk_key)


    return render(request,'case/new.html')


#-------------一個CASE的詳細資訊-------------
@login_required
def case_profile(request ,case_id):
    user = get_object_or_404(  # 找出這個 user; 找不到則回傳 404 error
        UserDetail,
        django_user=request.user,
        isActive=True)  # 若是被停權的 user，一樣 404

    pk_key = case_id

    #瀏覽人數+1
    temp_case = Case.objects.get(case_id=pk_key)
    temp_case.pageviews += 1
    temp_case.save()

    # 讀出case 資訊
    list_case = Case.objects.filter(Q(case_id=pk_key) & Q(shown_public=True))
    case_fields = Case_Field.objects.filter(case = pk_key)
    case_types = Case_Type.objects.filter(case = pk_key)
    case_photo = CasePhoto.objects.filter(case = pk_key)

    # 讀出使用者資訊
    temp_user = Case.objects.get(Q(case_id=pk_key) & Q(shown_public=True))
    user_id = temp_user.publisher.user_id
    user_detail = UserDetail.objects.filter(user_id = user_id)

    # user can take or not
    user = request.user.user_detail
    case = Case.objects.get(Q(case_id=pk_key))
    button_status = 0
    try:
        CommissionRecord.objects.get(Q(commissioned_user=user) & Q(case=case))
    except:
        try:
            CaseWillingness.objects.get(Q(willing_user=user) & Q(apply_case=case))
        except:
            button_status = 1  # can sign up the case
        else:
            button_status = 2  # show "cancel the case"
    else:
        button_status = 3  # cannot press the button never

    return render(request,'case/profile.html',locals())


#-------------一個CASE的編輯資訊-------------
@login_required
def case_profile_edit(request,case_id):
    user = get_object_or_404(  # 找出這個 user; 找不到則回傳 404 error
        UserDetail,
        django_user=request.user,
        isActive=True)  # 若是被停權的 user，一樣 404

    pk_key = case_id
    user_id = request.user.user_detail.user_id
    # 找出哪一筆case
    case = Case.objects.get(case_id=pk_key)

    # 確認是不是case的發布人
    if case.publisher.user_id == user_id:

        if request.method == "POST" :

            # post 接值case委託資訊
            title = request.POST.get('title')
            description = request.POST.get('description')
            reward = request.POST.get('reward')
            num = request.POST.get('num')
            work = request.POST.get('work')
            location = request.POST.get('location')
            constraint = request.POST.get('constraint')
            ended_datetime = request.POST.get('ended_datetime')

            # 找出哪一筆case
            update_case = Case.objects.get(case_id=pk_key)

            # update case table 參數
            update_case.title = title
            update_case.description = description
            update_case.reward = reward
            update_case.num = num
            update_case.work = work
            update_case.location = location
            update_case.constraint = constraint
            update_case.ended_datetime = ended_datetime
            update_case.save()


            # update casephote & Case_Type & Case_Field
            # 外部鍵:多對多: 抓取哪一筆資料
            case = Case.objects.get(case_id=pk_key)

            # 直接刪除 類型 原本的資料
            CasePhoto.objects.filter(case = pk_key).delete()

            image = request.FILES.getlist('photo_image')
            for f in image:
                file = CasePhoto(image=f, case = case)
                file.save()


            # 直接刪除 類型 原本的資料
            Case_Type.objects.filter(case = pk_key).delete()
            # 類型
            type_temp = request.POST.getlist('case_type')
            for i in range(len(type_temp)):
                type = Type.objects.get(type_id = type_temp[i])
                case_type = Case_Type(case_type = type, case = case )
                case_type.save()


            # 直接刪除 領域 的資料
            Case_Field.objects.filter(case = pk_key).delete()
            # 領域
            field_temp = request.POST.getlist('case_field')
            for i in range(len(field_temp)):
                field = Field.objects.get(field_id = field_temp[i])
                case_field = Case_Field(case_field = field ,case = case)
                case_field.save()


            # 顯示的data
            list_case = Case.objects.filter(Q(case_id=pk_key) & Q(shown_public=True))
            case_fields = Case_Field.objects.filter(case = pk_key)
            case_types = Case_Type.objects.filter(case = pk_key)
            case_photo = CasePhoto.objects.filter(case = pk_key)

            return redirect('case-profile',case_id = pk_key)


        list_case = Case.objects.filter(Q(case_id=pk_key) & Q(shown_public=True))
        case_fields = Case_Field.objects.filter(case = pk_key)
        case_types = Case_Type.objects.filter(case = pk_key)
        case_photo = CasePhoto.objects.filter(case = pk_key)

        nolist_case = Case.objects.get(Q(case_id=pk_key) & Q(shown_public=True))
        title = nolist_case.title

        return render(request,'case/profile_edit.html',locals())


    # 不是該case的發布人無權限編輯
    else :
        messages.warning(request, "You don't have right to edit the case.")
        return redirect('index')


# -------------CASE資訊搜尋-------------
@login_required
def case_search(request):
    user = get_object_or_404(  # 找出這個 user; 找不到則回傳 404 error
        UserDetail,
        django_user=request.user,
        isActive=True)  # 若是被停權的 user，一樣 404

    list_case = Case.objects.filter(shown_public=True)
    case_fields = Case_Field.objects.all()
    case_types = Case_Type.objects.all()
    case_photo = CasePhoto.objects.all()


    #list_case = Case.objects.select_related('case_status')
    return render(request,'case/search.html',locals()) #之後要改



#####################################
#            USER MODULE            #
#####################################
# ------ 使用者資料頁面 ------
@login_required
def viewUser(request):
    user = get_object_or_404(  # 找出這個 user; 找不到則回傳 404 error
        UserDetail,
        django_user=request.user,
        isActive=True)  # 若是被停權的 user，一樣 404

    # 更改使用者資料的表單
    userDataForm = UserDetailModelForm(instance=user)
    print(f'get data of {user}.')

    # 取得使用者資料
    dataCol = [  # 要取得哪些欄位 #目前沒作用
        'name',
        'nickname',
        'account_mail',
        'gender',
        'department',
        'work',
        'information',
        'icon',
        'rate',
        'rate_num',
        'work_num',
        'publish_num',
        'commissioned_status',
        'commissioning_status',
        'verification',
        'created_datetime',
        'last_login_datetime'
        ]

    # 整理資訊並回傳
    content = {  # 要傳入模板的資訊
        'user': user,
        'userDataForm': userDataForm,
        }
    return render(request, 'user/user.html', content)


# ------ 更新使用者資料 ------
@login_required
def updateUser(request):
    user = get_object_or_404(  # 找出這個 user; 找不到則回傳 404 error
        UserDetail,
        django_user=request.user,
        isActive=True)  # 若是被停權的 user，一樣 404
    userDataForm = UserDetailModelForm(instance=user)  # 預計要傳的表單資料

    # POST: 更改使用者資料
    if request.method == 'POST':
        print('\n\nrequest.POST:', request.POST)
        formPost = UserDetailModelForm(request.POST, instance=user)
        if formPost.is_valid():
            userUpdate = formPost.save(commit=False)  # 先暫存，還不更改資料庫
            userUpdate.account_mail = user.account_mail  # 自動填入email
            userUpdate.save()  # 實際更改資料庫
            print('User data has been update.')
            return redirect('user-profile')  # 重定向並刷新個資分頁的資訊
        else:
            print('The form is not valid.')
            userDataForm = formPost  # 保留剛剛POST的分析結果，以顯示錯誤訊息

    # 整理資訊並回傳
    content = {  # 要傳入模板的資訊
        'user': user,
        'userDataForm': userDataForm,
        }
    return render(request, 'user/user.html/', content)


# ------ 更新使用者頭像 ------
@login_required
def updateUserIcon(request):
    user = get_object_or_404(  # 找出這個 user; 找不到則回傳 404 error
        UserDetail,
        django_user=request.user,
        isActive=True)  # 若是被停權的 user，一樣 404
    userDataForm = UserDetailModelForm(instance=user)  # 預計要傳的表單資料

    # POST: 更改使用者資料
    if request.method == 'POST':
        print('\n\nrequest.POST:', request.POST)
        print('request.FILES:', request.FILES)
        iconPost = UserIconForm(request.POST, instance=user)  # 改頭像的表單
        if iconPost.is_valid():
            userUpdate = iconPost.save(commit=False)  # 先暫存，還不更改資料庫
            userUpdate.name = user.name  # 自動填入name
            userUpdate.account_mail = user.account_mail  # 自動填入email
            if request.FILES:  # 若有上傳圖片
                try:
                    if userUpdate.icon:  # 若有舊檔，就刪除
                        try:
                            oldUrl = userUpdate.icon.url[1:]  # 去掉最前面的斜線
                            oldUrl = os.path.join(django_settings.BASE_DIR, oldUrl)
                            print('find old icon and remove file', oldUrl)
                            os.remove(oldUrl)
                        except Exception as ex:
                            print('Cannot remove old file:', ex)
                    userUpdate.icon = request.FILES['icon']
                except Exception as ex:
                    print('Can not save user icon:', ex)
            userUpdate.save()  # 實際更改資料庫
            print('User data has been update.')
            return redirect('user-profile')  # 重定向並刷新個資分頁的資訊
        else:
            print('The form is not valid.')
            userDataForm = iconPost  # 保留剛剛POST的分析結果，以顯示錯誤訊息

    # 整理資訊並回傳
    content = {  # 要傳入模板的資訊
        'user': user,
        'userDataForm': userDataForm,
        }
    return render(request, 'user/user.html/', content)
    # number of visits to this view
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # return user name
    user_name = UserDetail.objects.get(Q(django_user=request.user))

    return render(
        request,
        'index.html',
        context={'num_visits': num_visits,
                 'user_name': user_name},
    )



# ------------user publish record------------
@login_required
def user_publish_record(request):

    timeout(request)

    # all case the user publish
    user = request.user.user_detail.user_id
    publisher = UserDetail.objects.get(user_id=user)
    case_list = Case.objects.filter(publisher=publisher)

    # time left
    deadline = {}
    for data in case_list:
        if data.case_status.status_id in [1, 2]:
            delta = data.ended_datetime - datetime.datetime.now().astimezone()
            if delta.days > 30:
                deadline[data.case_id] = f"{delta.days // 30} 個月"
            elif delta.days > 0:
                deadline[data.case_id] = f"{delta.days} 天"
            elif delta.seconds > 3600:
                deadline[data.case_id] = f"{delta.seconds // 3600} 小時"
            else:
                deadline[data.case_id] = "不到一小時"

    # show all of the toolmen
    record_list = CommissionRecord.objects.all().prefetch_related('case')
    willing_list = CaseWillingness.objects.all().prefetch_related('apply_case')

    # numbers of toolmen for each case
    # average rate for each case
    number = dict()
    avg_rate = dict()
    for case in case_list:
        if case.case_status.status_id in [1, 2]:
            number[case.case_id] = 0
            for record in record_list:
                if record.case == case and record.user_status.status_id != 4:
                    number[case.case_id] += 1
        elif case.case_status.status_id in [3, 4]:
            avg_rate[case.case_id] = 0
            cnt = 0
            for record in record_list:
                if record.case == case and record.rate_worker_to_publisher != None:
                    avg_rate[case.case_id] += record.rate_worker_to_publisher
                    cnt += 1
                if cnt != 0:
                    avg_rate[case.case_id] /= cnt

    # check the status should turn back to 1 or not
    for key, value in number.items():
        if value == 0:
            case = Case.objects.get(Q(case_id=key))
            case.case_status = Status.objects.get(Q(status_id=1))
            case.save()

    # number of applicants
    willing = dict()
    for case in case_list:
        willing[case.case_id] = 0
        for data in willing_list:
            if data.apply_case == case:
                try:
                    CommissionRecord.objects.get(Q(commissioned_user=data.willing_user) & Q(case=case))
                except:
                    willing[case.case_id] += 1               
    
    return render(request, 'user/publish.html', locals())


# ---------applicants for each case---------
@login_required
def user_publish_applicant(request, case_id):

    timeout(request)

    # all applicants for all cases
    case = Case.objects.get(Q(case_id=case_id))
    all_willing = CaseWillingness.objects.all().prefetch_related('apply_case').filter(apply_case=case)
    all_commission = CommissionRecord.objects.filter(case=case)

    # is commissioned or not
    all_user = set()
    willingness = []
    cnt = 0
    for data in all_willing:  # pick the newest one for all users
        all_user.add(data.willing_user)
    for user in all_user:
        newest_willing = all_willing.filter(willing_user=user).order_by('-created_datetime')[0]
        newest_commission = all_commission.filter(commissioned_user=user).order_by('-created_datetime')
        if len(newest_commission) == 0:  # commissioned not yet
            willingness.append(newest_willing)
        elif newest_willing.created_datetime > newest_commission[0].created_datetime:  # a new willingness
            willingness.append(newest_willing)

    # count the number of conducting user
    for user in all_user:
        commission = CommissionRecord.objects.filter(Q(case=case) & Q(commissioned_user=user))
        for record in commission:
            if record.user_status.status_id != 4:
                cnt += 1
    last = case.num - cnt

    return render(request, 'user/applicant.html', locals())



# ------------user take record------------
@login_required
def user_take_record(request):

    timeout(request)

    # all willingness the user takes
    user = request.user.user_detail
    all_willing = CaseWillingness.objects.all().prefetch_related('apply_case').filter(willing_user=user)
    all_commission = CommissionRecord.objects.filter(Q(commissioned_user=user))

    # is commissioned or not
    all_case = set()
    willingness = []
    for data in all_willing:  # all cases
        all_case.add(data.apply_case)
    for case in all_case:  # pick the newest one for all cases
        newest_willing = all_willing.filter(apply_case=case).order_by('-created_datetime')[0]
        newest_commission = all_commission.filter(case=case).order_by('-created_datetime')
        if len(newest_commission) == 0:  # commissioned not yet
            willingness.append(newest_willing)
        elif newest_willing.created_datetime > newest_commission[0].created_datetime:  # a new willingness
            willingness.append(newest_willing)

    # all commissions the user takes
    record = CommissionRecord.objects.all().prefetch_related('case').filter(commissioned_user=user)
    conduct = []
    close = []
    deadline = {}
    for data in record:
        status = data.user_status.status_id
        if status == 2 or status == 5 or status == 6 or status == 7:
            conduct.append(data)
            if status == 2:
                delta = data.case.ended_datetime - datetime.datetime.now().astimezone()
                if delta.days > 30:
                    deadline[data.commissionrecord_id] = f"{delta.days // 30} 個月"
                elif delta.days > 0:
                    deadline[data.commissionrecord_id] = f"{delta.days} 天"
                elif delta.seconds > 3600:
                    deadline[data.commissionrecord_id] = f"{delta.seconds // 3600} 小時"
                else:
                    deadline[data.commissionrecord_id] = "不到一小時"
        elif status == 3 or status == 4:
            close.append(data)

    return render(request, 'user/take.html', locals())



#########################################
#           USER-CASE  MODULE           #
#########################################

# ---------tool man sign up cases---------
@login_required
def take_case(request, case_id):

    # foreign key
    case = Case.objects.get(Q(case_id=case_id))
    user = UserDetail.objects.get(Q(django_user=request.user))
    
    # create a case willingness
    willingness = CaseWillingness.objects.create(apply_case=case, willing_user=user)
    willingness.save()

    return redirect('case-profile', case_id=case_id)


# ---------cancel willingness for case---------
@login_required
def cancel_willingess(request, case_id):
    
    case = Case.objects.get(Q(case_id=case_id))
    user = request.user.user_detail
    try:
        willingness = CaseWillingness.objects.get(Q(apply_case=case) & Q(willing_user=user))
        willingness.delete()
    except:
        pass

    button_status = 1

    return render(request,'case/profile.html',locals())



# ---------cancel willingness for user---------
@login_required
def user_cancel_willingess(request, case_id):
    
    case = Case.objects.get(Q(case_id=case_id))
    user = request.user.user_detail
    try:
        willingness = CaseWillingness.objects.get(Q(apply_case=case) & Q(willing_user=user))
        willingness.delete()
    except:
        pass

    messages.info(request, 'take_sign', extra_tags='origin_page')
    return redirect('user-take-record')



# ---------build commission---------
@login_required
def build_commission(request):
    
    try:
        # get case willingness id
        body = request.body.decode('utf-8').split('&toolman=')[1:]
        toolmanInfoList = []

        # create commission record
        for id in body:
            willingness = CaseWillingness.objects.get(Q(casewillingness_id=id))
            case = willingness.apply_case
            toolman = willingness.willing_user
            status = Status.objects.get(Q(status_id=2))
            toolmanInfoList.append(willingness.willing_user)

            record = CommissionRecord.objects.create(case=case,
                                                     commissioned_user=toolman,
                                                     user_status=status)
            record.save()

        # create notice for publisher
        msg = f"您已對 案件編號#{case.case_id} {case.title} 成立委託，請至 我的委託 查看工具人聯繫方式。"
        notice = Notice.objects.create(user=request.user.user_detail, message=msg)
        notice.save()

        # create notice for all toolmen
        msg = f"案件編號#{case.case_id} {case.title}，委託人 {request.user.user_detail.nickname} 已成立委託，請至 我的接案 查看委託人聯繫方式。"
        for user in toolmanInfoList:
            notice = Notice.objects.create(user=user, message=msg)
            notice.save()

        # change case status
        case.case_status = Status.objects.get(Q(status_id=2))
        case.save()

        messages.info(request, case.case_id, extra_tags='origin_case')

    except:
        # choose nobody
        pass

    messages.info(request, 'publish', extra_tags='origin_page')
    return redirect('user-publish-record')



# ---------delete commission---------
@login_required
def delete_commission(request, commission_id):

    # set sender/receiver as publisher or toolman
    commission = CommissionRecord.objects.get(Q(commissionrecord_id=commission_id))
    case = commission.case
    messages.info(request, case.case_id, extra_tags='origin_case')

    # first time cancel
    if commission.user_status.status_id == 2:
        sender = request.user.user_detail
        if commission.commissioned_user == sender:
            receiver = commission.case.publisher
            commission.user_status = Status.objects.get(Q(status_id=6))
            commission.finish_datetime = datetime.datetime.now()
            commission.save()
        else:
            receiver = commission.commissioned_user
            commission.user_status = Status.objects.get(Q(status_id=5))
            commission.finish_datetime = datetime.datetime.now()
            commission.save()

        if sender == commission.commissioned_user:
            messages.info(request, 'taking', extra_tags='origin_page')
            return redirect('user-take-record')
        else:
            messages.info(request, 'publish', extra_tags='origin_page')
            return redirect('user-publish-record')

    # both cancel the case
    elif commission.user_status.status_id == 5:
        sender = commission.commissioned_user
        receiver = commission.case.publisher
    elif commission.user_status.status_id == 6:
        sender = commission.case.publisher
        receiver = commission.commissioned_user
    commission.user_status = Status.objects.get(Q(status_id=4))
    commission.doublecheck_datetime = datetime.datetime.now()
    commission.save()

    # if there is no commission, change the case status
    close_status = Status.objects.get(Q(status_id=4))
    result = CommissionRecord.objects.filter(Q(case=case) & ~Q(user_status=close_status))
    if result.exists():
        pass
    else:
        case.case_status = Status.objects.get(Q(status_id=1))
        case.save()
    
    if sender == commission.commissioned_user:
        messages.info(request, 'taking', extra_tags='origin_page')
        return redirect('user-take-record')
    else:
        messages.info(request, 'publish', extra_tags='origin_page')
        return redirect('user-publish-record')


# ---------finish commission---------
@login_required
def finish_commission(request, commission_id):

    commission = CommissionRecord.objects.get(Q(commissionrecord_id=commission_id))
    messages.info(request, commission.case.case_id, extra_tags='origin_case')

    # status=2 represent that toolman apply for consummation
    if commission.user_status.status_id == 2:

        # change status
        commission.user_status = Status.objects.get(Q(status_id=7))
        commission.finish_datetime = datetime.datetime.now()
        commission.save()

        messages.info(request, 'taking', extra_tags='origin_page')

        return redirect('user-take-record')

    # status=7 represent that publisher confirm the task
    else:

        # change status
        commission.user_status = Status.objects.get(Q(status_id=3))
        commission.doublecheck_datetime = datetime.datetime.now()
        commission.save()

        messages.info(request, 'publish', extra_tags='origin_page')

        return redirect('user-publish-record')



# ---------give rate---------
@login_required
def rate(request):

    # get id and rate from request body
    body = request.body.decode('utf-8').split('&')
    for data in body:
        try:
            int(data.split('=')[0])
        except:
            pass
        else:
            id = int(data.split('=')[0])
            rate = int(data.split('=')[1])
            break

    commission = CommissionRecord.objects.get(Q(commissionrecord_id=id))
    user = request.user.user_detail
    messages.info(request, commission.case.case_id, extra_tags='origin_case')

    # publisher gives rating for toolman
    if user == commission.case.publisher:
        commission.rate_publisher_to_worker = rate
        commission.save()

        toolman = commission.commissioned_user
        ori_rate = toolman.rate * toolman.rate_num
        new_rate = (ori_rate + rate) / (toolman.rate_num + 1)
        toolman.rate  = new_rate
        toolman.rate_num  = toolman.rate_num + 1
        toolman.save()

        if commission.case.case_status.status_id in [3, 4]:
            messages.info(request, 'publish_his', extra_tags='origin_page')
        else:
            messages.info(request, 'publish', extra_tags='origin_page')

        return redirect('user-publish-record')

    # toolman gives rating for publisher
    else:
        commission.rate_worker_to_publisher = rate
        commission.save()

        publisher = commission.case.publisher
        ori_rate = publisher.rate * publisher.rate_num
        new_rate = (ori_rate + rate) / (publisher.rate_num + 1)
        publisher.rate  = new_rate
        publisher.rate_num  = publisher.rate_num + 1
        publisher.save()

        if commission.user_status.status_id in [3, 4]:
            messages.info(request, 'take_his', extra_tags='origin_page')
        else:
            messages.info(request, 'taking', extra_tags='origin_page')

        return redirect('user-take-record')



#########################################
#              AUTH MODULE              #
#########################################

# ----------------login------------------
def login(request):

    # check mail validation
    if 'first_refresh' in request.session and request.session['first_refresh'] == False:
        request.session['first_refresh'] = True
        return redirect('register')

    # check url timeout or not
    all_user = User.objects.all()
    for data in all_user:
        if data.user_detail.isActive == False:
            if (datetime.datetime.now().astimezone() -  data.date_joined).seconds > 3600:
                user_detail = UserDetail.objects.get(Q(django_user=data))
                user_detail.delete()
                data.delete()

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
                messages.warning(request,'帳號尚未啟用')
                return redirect('login')

            # check suspended or not
            isActive = userDetail.isActive
            if not isActive:
                messages.warning(request,'帳號已停權')
                return redirect('login')

            # login and create session
            auth.login(request, user)
            return HttpResponseRedirect('home/')

        # send error message
        elif account != "":
            messages.warning(request,'使用者帳號或密碼錯誤')
        return redirect('login')

    return render(request, 'auth/login.html', locals())


# -----------customize authentication-----------
class CustomizeUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            django_user = User.objects.get(Q(email=username))
        except User.DoesNotExist as e:
            return None
        if check_password(password, django_user.password):
            return django_user


# ----------------logout------------------
def logout(request):

    auth.logout(request)
    return HttpResponseRedirect('/')


# ----------------register------------------
def register(request):

    # check email validation
    if 'mail_validation' in request.session:
        mailserver = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        mailserver.login(django_settings.EMAIL_HOST_USER, django_settings.EMAIL_HOST_PASSWORD)
        status, count1 = mailserver.select('Inbox')
        time.sleep(2)
        status, count2 = mailserver.select('Inbox')
        status, data = mailserver.fetch(count2[0], '(UID BODY[TEXT])')
        ori_mail = data[0][1].decode('utf-8').split('<')[1].split('>')[0]
        mailserver.close()
        mailserver.logout()

        if ori_mail == request.session['mail_validation']:
            ori_user = User.objects.get(Q(email=ori_mail))
            ori_user.delete()

            request.session['messages'] = "對不起，您使用的註冊信箱無效。\n請確認信箱後重新註冊。"
            del request.session['mail_validation']
            del request.session['first_refresh']
            return HttpResponseRedirect('/')

        request.session['messages'] = "請查看信箱點擊連結以完成註冊驗證。\n連結有效期為1個小時。"
        del request.session['mail_validation']
        del request.session['first_refresh']
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        account = request.POST.get('account')
        password = request.POST.get('password')

        # send verification url to user email
        token = token_confirm.generate_validate_token(username)
        if request.META['HTTP_HOST'] == "127.0.0.1:8000":
            url = 'http://' + request.META['HTTP_HOST'] + '/toolfamily/activate/' + token
        else:
            url = 'https://' + request.META['HTTP_HOST'] + '/toolfamily/activate/' + token

        title = "NTU TOOLBOX 註冊驗證"
        msg = "歡迎加入 NTU TOOLBOX! 請點選下方連結完成註冊驗證。\n" + url
        email_from = django_settings.DEFAULT_FROM_EMAIL
        receiver = [account]

        try:
            send_mail(title, msg, email_from, receiver, fail_silently=False)
            request.session['mail_validation'] = account
            request.session['first_refresh'] = False
        except:
            messages.warning(request,'信箱格式錯誤或已註冊')
            return redirect('register')

        # insert user detail into User
        user = User.objects.create_user(username=username, password=password, email=account, is_active=False)
        user.save()

        # insert user detail into UserDetail
        userDetail = UserDetail.objects.create(name=username, django_user=user, account_mail=account, salt=password)
        userDetail.save()

        return HttpResponseRedirect('/')

    return render(request, 'auth/register.html', locals())


# ------------email verification-------------
def active(request, token):

    # timeout
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        try:
            user = User.objects.get(Q(username=username))
            userDetail = UserDetail.objects.get(Q(django_user=user))
            userDetail.delete()
            user.delete()
        except:
            pass
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
        account = request.POST.get('account')
        print(account)
        try:
            user = UserDetail.objects.get(Q(account_mail=account))
            print(user)
            username = user.name

            # send reset-pwd url to user email
            token = token_confirm.generate_validate_token(username)
            if request.META['HTTP_HOST'] == "127.0.0.1:8000":
                url = 'http://' + request.META['HTTP_HOST'] + '/toolfamily/reset/' + token
            else:
                url = 'https://' + request.META['HTTP_HOST'] + '/toolfamily/reset/' + token

            title = "NTU TOOLBOX 重新設定密碼"
            msg = "請點選下方連結重新設定密碼。\n" + url
            email_from = django_settings.DEFAULT_FROM_EMAIL
            receiver = [account]
            send_mail(title, msg, email_from, receiver, fail_silently=False)

            request.session['messages'] = "請查看信箱點擊連結並重新設定密碼。\n連結有效期為1個小時。"
            return HttpResponseRedirect('/')

        except:
            messages.warning(request,'帳號不存在')
            return redirect('forget')

    return render(request, 'auth/forget_pwd.html', locals())


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
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        # update datebase
        user = User.objects.get(Q(username=username))
        user.password = make_password(password)
        user.save()

        userDetail = UserDetail.objects.get(Q(django_user=user))
        userDetail.salt = user.password
        userDetail.save()

        request.session['messages'] = "密碼更改成功！"
        return HttpResponseRedirect('/')

    return render(request, 'auth/reset_pwd.html', locals())


# -----------check register email-------------
@csrf_exempt
def check_mail_used(request):

    # parse json
    account = json.loads(request.body).get('email')

    try:
        user = UserDetail.objects.get(Q(account_mail=account))
        return JsonResponse({"message": ""})
    except:
        return JsonResponse({"message": "帳號未被使用"})