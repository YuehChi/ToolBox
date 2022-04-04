from django.shortcuts import render ,redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from django.db.models import Q

# Create your views here.
def index(request):
   
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,'index.html',context={'num_visits': num_visits},
    )




#####################################
#           CASE MODULE             #
#####################################

#-------------新增CASE---------------
@login_required
def case_new(request):

    ### 登入權限判斷
    # if not request.user.is_authenticated:
    #    return render(request,'index.html')
    
    # else:

    if request.method == "POST" :

        #委託人-外部鍵
        publisher = UserDetail.objects.get(user_id = "4")

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

    return render(request,'case/profile.html',locals())




#-------------一個CASE的編輯資訊-------------
@login_required
def case_profile_edit(request,case_id):

    pk_key = case_id

    if request.method == "POST" :

        # post 接值case委託資訊
        title = request.POST.get('title')
        description = request.POST.get('description')
        reward = request.POST.get('reward')
        location = request.POST.get('location')
        constraint = request.POST.get('constraint')

        # 找出哪一筆case
        update_case = Case.objects.get(case_id=pk_key)
  
        # update case table 參數
        update_case.title = title
        update_case.description = description
        update_case.reward = reward
        update_case.location = location
        update_case.constraint = constraint
        update_case.save()


        # 照片 
        image = request.FILES.get('photo_image')
        casephoto = CasePhoto(case = pk_key)
        casephoto.image = image
        casephoto.save()

        # 類型
        type_temp = request.POST.getlist('case_type')
        for i in range(len(type_temp)):
            type = Type.objects.get(type_id = type_temp[i])
            case_type = Case_Type(case = pk_key)
            case_type = type
            case_type.save()

        # 領域 
        field_temp = request.POST.getlist('case_field')
        for i in range(len(field_temp)):
            field = Field.objects.get(field_id = field_temp[i])
            case_field = Case_Field(case = pk_key)
            case_field = field
            case_field.save()

        # 顯示的data
        list_case = Case.objects.filter(Q(case_id=pk_key) & Q(shown_public=True))  
        case_fields = Case_Field.objects.filter(case = pk_key)  
        case_types = Case_Type.objects.filter(case = pk_key)   
        case_photo = CasePhoto.objects.filter(case = pk_key)   
        
        return render(request,'case/profile.html',locals())


    list_case = Case.objects.filter(Q(case_id=pk_key) & Q(shown_public=True))  
    case_fields = Case_Field.objects.filter(case = pk_key)  
    case_types = Case_Type.objects.filter(case = pk_key)   
    case_photo = CasePhoto.objects.filter(case = pk_key)

    nolist_case = Case.objects.get(Q(case_id=pk_key) & Q(shown_public=True)) 
    title = nolist_case.title 

    return render(request,'case/profile_edit.html',locals())

# -------------CASE資訊搜尋-------------
@login_required
def case_search(request):

    list_case = Case.objects.filter(shown_public=True)
    case_fields = Case_Field.objects.all()
    case_types = Case_Type.objects.all()
    case_photo = CasePhoto.objects.all()


    #list_case = Case.objects.select_related('case_status')
    return render(request,'case/search.html',locals()) #之後要改



