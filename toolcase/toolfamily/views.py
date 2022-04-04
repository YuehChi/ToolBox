from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required



def index(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1
    # user data
    userData = {'nickname': '您尚未登入'}
    if request.user.is_authenticated:  # if the user has login
        userData = {
            'nickname': request.user.user_detail.nickname,
            'icon': request.user.user_detail.icon,
            }
    print('userData:', userData)

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context = {
            'num_visits': num_visits,
            'user': userData,},
    )



#####################################
#           USER VIEWS              #
#####################################
# 使用者資料頁面
@login_required
def viewUser(request):
    user = get_object_or_404(  # 找出這個 user; 找不到則回傳 404 error
        UserDetail,
        django_user=request.user,
        isActive=True)  # 若是被停權的 user，一樣 404
    userDataForm = ''  # 預計要傳 html 表單；非 POST 或 GET 則為空
    content = {}  # 要傳入模板的資訊

    # POST: 更改使用者資料
    if request.method == 'POST':
        print('\n\n\nrequest.POST:', request.POST)
        formPost = UserDetailModelForm(request.POST, instance=user)
        if formPost.is_valid():
            userUpdate = formPost.save(commit=False)  # 先暫存，還不更改資料庫
            userUpdate.account_mail = user.account_mail  # 自動填入email
            if request.FILES:  # 若有上傳圖片
                try:
                    oldIconUrl = userUpdate.icon.url
                    userUpdate.icon = request.FILES['icon']
                except Exception as ex:
                    print('Can not save user icon:', ex)
            userUpdate.save()  # 實際更改資料庫
            print('User data has been update.')
            return redirect('user-profile')
        else:
            print('The form is not valid.')
            userDataForm = userUpdate  # 保留剛剛POST的分析結果，以顯示錯誤訊息

    # GET: 取得使用者資料
    elif request.method == 'GET':
        # 更改使用者資料的表單
        userDataForm = UserDetailModelForm(instance=user)
        print(f'get data of {user}:', userDataForm)
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

    content = {
        'user': user,
        'userDataForm': userDataForm,
        }
    return render(request, 'user/user.html', content)
