from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from .models import *

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

        case = Case(title = title ,publisher = publisher, description = description , reward = reward, location = location , 
        constraint = constraint, started_datetime = started_datetime , ended_datetime = ended_datetime,case_status =case_status)
        case.save()


        # 外部鍵 case (抓最新一筆關聯)
        case = Case.objects.first()

        # 照片
            
        image = request.FILES.get('photo_image')
        casephoto = CasePhoto(image = image , case = case)
        casephoto.save()

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

        return render(request,'case/case_all_temp.html') 

   

    return render(request,'case/new.html')

#-------------詳細CASE資訊-------------
def case_profile(request):

    context ={

    }

    return render(request,'case/profile.html',context=context)


#-------------編輯CASE資訊-------------
def case_profile_edit(request):

    context ={

    }

    return render(request,'case/profile_edit.html',context=context)

# -------------CASE資訊搜尋-------------
@login_required
def case_search(request):

    list_case = Case.objects.filter(shown_public=True)
    case_fields = Case_Field.objects.all()
    case_types = Case_Type.objects.all()
    case_photo = CasePhoto.objects.all()


    #list_case = Case.objects.select_related('case_status')
    return render(request,'case/search.html',locals()) #之後要改



#---------------temp--------------

#-------------新增CASE---------------
@login_required
def case_new_temp(request):

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

        case = Case(title = title ,publisher = publisher, description = description , reward = reward, location = location , 
        constraint = constraint, started_datetime = started_datetime , ended_datetime = ended_datetime,case_status =case_status)
        case.save()


        # 外部鍵 case (抓最新一筆關聯)
        case = Case.objects.first()

        # 照片
            
        image = request.FILES.get('photo_image')
        casephoto = CasePhoto(image = image , case = case)
        casephoto.save()

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

        return render(request,'case/case_all_temp.html') 

   

    return render(request,'case/new_temp.html')





@login_required
def case_all_temp(request):

    list_case = Case.objects.filter(shown_public=True)
    case_fields = Case_Field.objects.all()
    case_types = Case_Type.objects.all()
    case_photo = CasePhoto.objects.all()


    #list_case = Case.objects.select_related('case_status')
    return render(request,'case/case_all_temp.html',locals()) #之後要改

