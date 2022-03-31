from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required



def index(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,'index.html', context={'num_visits': num_visits},
    )



#####################################
#           USER VIEWS              #
#####################################
# 使用者資料頁面
@login_required
def viewUser(request):
    print('viewUser')
    user = get_object_or_404(  # 找出這個 user; 找不到則回傳 404 error
        UserDetail,
        django_user=request.user,
        isActive=True)  # 若是被停權的 user，一樣 404
    userDataForm = ''  # 預計要傳 html 表單；非 POST 或 GET 則為空

    # POST: 更改使用者資料
    if request.method == 'POST':
        formPost = UserDetailModelForm(request.POST, instance=user)
        if formPost.is_valid():
            formPost.save()
            print('update in view!gogo!')
            return redirect('user-profile')
        else:
            print('The form is not valid.')
            userDataForm = formPost  # 保留剛剛POST的分析結果，以顯示錯誤訊息

    # GET: 取得使用者資料
    elif request.method == 'GET':
        # 更改使用者資料的表單
        userDataForm = UserDetailModelForm(instance=user)
        print(f'get data of {user}')
        # 取得使用者資料
        dataCol = [  # 要取得哪些欄位
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
            'commissioned_status',
            'commissioning_status',
            'verification',
            'created_datetime',
            'last_login_datetime'
            ]

    return render(request, 'user.html', locals())
