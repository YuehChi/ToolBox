from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from .forms import *
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
import os  # 為了在上傳新檔時刪除舊檔
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages, auth
import django, json, smtplib
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.backends import ModelBackend
import base64
from itsdangerous import URLSafeTimedSerializer as utsr
from django.conf import settings as django_settings
from django.core.mail import send_mail
from datetime import date , datetime ,timedelta
from django.utils.timezone import now
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def calPage (data_list , page):

    paginator = Paginator(data_list,10)
    count_page = paginator.num_pages
    try:
        totalpage_length = paginator.page(page)
    except PageNotAnInteger:
        totalpage_length = paginator.page(1)
    except EmptyPage:
        totalpage_length = paginator.page(paginator.num_pages)

    return totalpage_length , count_page

def calPage_index (data_list , page):

    paginator = Paginator(data_list,5)
    count_page = paginator.num_pages
    try:
        totalpage_length = paginator.page(page)
    except PageNotAnInteger:
        totalpage_length = paginator.page(1)
    except EmptyPage:
        totalpage_length = paginator.page(paginator.num_pages)

    return totalpage_length, count_page


@login_required
def index(request):
   
    # 最新的case
    new_case = Case.objects.filter(shown_public=True)
    page_new = request.GET.get('page_new', 1)
    new_case , num_pages = calPage_index(new_case,page_new)
    
    # 最多瀏覽的case
    page_most = request.GET.get('page_most', 1)
    most_case = Case.objects.filter(shown_public=True).order_by('-pageviews')
    most_case , num_pages = calPage_index(most_case,page_new)

    case_fields = Case_Field.objects.all()
    case_types = Case_Type.objects.all()
    case_photo = CasePhoto.objects.all()

    return render(request,'index.html',locals()) #之後要改

# 合併5張表 
#   list_case = Case.objects.filter(shown_public=True)
#     case_fields = Case_Field.objects.all()
#     case_types = Case_Type.objects.all()
#     case_photo = CasePhoto.objects.all()
    
#     case_detail = {}

#     for i in case_fields:
#         for j in case_types:
#             for k in case_photo:
#                 if i.case_id == j.case_id == k.case_id:
#                         case_detail = {
#                         "case_id" : i.case_id ,
#                         "title" : i.case.title,
#                         "publisher" :i.case.publisher,
#                         "reward" :i.case.reward,
#                         "num" :i.case.num,
#                         "work" :i.case.work,
#                         "pageviews" :i.case.pageviews,
#                         "location" :i.case.location,
#                         "description" :i.case.description,
#                         "constraint" :i.case.constraint,
#                         "started_datetime" :i.case.started_datetime,
#                         "ended_datetime" :i.case.ended_datetime,
#                         "case_status" :i.case.case_status.status_name ,
#                         "case_field" :i.case_field.field_name,
#                         "case_type" :j.case_type.type_name ,
#                         "image" : k.image,
#                         }

#####################################
#           CASE MODULE             #
#####################################

#-------------新增CASE---------------
@login_required
def case_new(request):

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

    pk_key = case_id
    check_user_id = request.user.user_detail.user_id

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

    alert = False
    pk_key = case_id
    user_id = request.user.user_detail.user_id
    # 找出哪一筆case
    case = Case.objects.get(case_id=pk_key)
    # print(case.case_status.status_id)
    # print(case.case_status.status_id == 1)

    # 確認是不是case的發布人
    if case.publisher.user_id == user_id and case.case_status.status_id == 1:

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
        alert = True
        erro =json.dumps("You don't have right to edit the case.")
        print("erro:",erro)
        print("alert:",alert)
        new_case = Case.objects.filter(shown_public=True)
        most_case = Case.objects.filter(shown_public=True).order_by('-pageviews')
        case_fields = Case_Field.objects.all()
        case_types = Case_Type.objects.all()
        case_photo = CasePhoto.objects.all()

        return render(request,'index.html',locals()) #之後要改
 

# -------------CASE資訊搜尋-------------
@login_required
def case_search(request):

    if request.method == "POST" :

        # 定義參數
        query_o = []
        vertify = 0 
        check = 0   #判斷是不是都沒填
        check2 = 0   #判斷是不是除了type和field 都沒有填
        alert = False
        erro = ''

        # 頁面資訊
        page = request.POST.get('page',1)

        # 查詢資訊資訊
        # == 單一查詢 ==
        query_o.append(request.POST.get('case_type'))
        query_o.append(request.POST.get('case_field'))
        query_o.append(request.POST.get('case_query'))
        for i in range(2):
            if query_o[i] == None:
                    vertify += 1 
        if query_o[2] == '':
            vertify += 1
        print("vertify:" , vertify)

        # == 複合查詢 ==
        type = request.POST.getlist('type')
        field = request.POST.getlist('field')
        num  = request.POST.get('num')
        date_time = request.POST.get('date_time')
        work = request.POST.get('work')
        constraint = request.POST.get('constraint')
        location = request.POST.get('location')

        # == 複合查詢- 是否要交集領域/類型 ==
        con = request.POST.get('con')  

        # == 複合查詢- 關鍵字 == 
        key= request.POST.get('query_list')
        print("*********key:",key)
        print(key == '' )
        print(key == None)
        query_list = [] 

        if key == None:
            query_list.append('')
        else : 
            key_arr = key.split(',')
            print(key_arr) 
            if key_arr [0] == '' :
                query_list = key_arr
            else:
                for s in key_arr:
                    query_list.append(int(s))
        print("query_list:",query_list) 
        print( query_list[0] != '' ) 

        if len(type) == 0 :
            check += 1
        if len(field) == 0 :
            check += 1
        if  num == '':
            num = 0
            check += 1
            check2 += 1
        if  work == '':
            work = 100000000000000000
            check += 1 
            check2 += 1
        if date_time == '':
            date_time = now().date() + timedelta(days=-1) 
            date_time = "2000-01-01"
            check += 1
            check2 += 1 
        if constraint =='':
            constraint = "None"
            check += 1
            check2 += 1 
        if location =='':
            location = "None"
            check += 1
            check2 += 1 

        print("check:" , check)
        print("check2:" , check2)
        print("Querry: " , query_o[0] ,query_o[1],query_o[2])
        print("Q: " , type ,field,num,date_time,work,constraint,location,con)
        print("========================================================")
    
        # == 單一查詢判斷 ==
        if vertify < 3: 
            # ==== 單一查詢 - 類型 ====
            if query_o[0] != None:
                print("single search for type :" ,query_o[1])
                id_list =[]
                case_types = Case_Type.objects.filter(case_type= query_o[0]).all()
                for i in case_types:
                    id_list.append(i.case_id)
                    print(i.case_id,i.case.title,i.case.publisher,i.case.case_status.status_name ,i.case_type.type_name)
                result_case = Case.objects.filter(case_id__in=id_list ).all()
                num_case = len(id_list)
                result_case, num_pages = calPage(result_case,page)
                case_fields = Case_Field.objects.filter(case_id__in=id_list ).all()
                case_photo = CasePhoto.objects.filter(case_id__in=id_list ).all()
                type_value = query_o[0]
                print("type_value:",type_value)
                print("id_list",id_list)
                print("num_case",num_case)

              
                return render(request,'case/search.html',locals())

            # ==== 單一查詢 - 領域 ====
            elif query_o[1] != None:
                print("single search for field :" ,query_o[1])
                id_list =[]
                case_fields = Case_Field.objects.filter(case_field=query_o[1] ).all()
                for i in case_fields:
                    id_list.append(i.case_id)
                    print(i.case_id,i.case.title,i.case.publisher,i.case.case_status.status_name ,i.case_field.field_name)
                result_case = Case.objects.filter(case_id__in=id_list ).all()
                num_case = len(id_list)
                result_case, num_pages = calPage(result_case,page)
                case_types = Case_Type.objects.filter(case_id__in=id_list ).all()
                case_photo = CasePhoto.objects.filter(case_id__in=id_list ).all()
                field_value = query_o[1]
                print("field_value:",field_value)
                print("id_list",id_list,"\n")
                
                return render(request,'case/search.html',locals()) 

            # ==== 單一查詢 - 關鍵字 ====
            else:
                print("single search for key_word :" ,query_o[2])
                id_list =[]
                query_list = []
                temp_case = Case.objects.filter(Q(title__icontains=query_o[2]) |  Q(description__icontains=query_o[2]) | 
                Q(reward__icontains=query_o[2]) | Q(location__icontains=query_o[2]) | Q(constraint__icontains=query_o[2])  & Q(shown_public=True) )
                for i in temp_case:
                    id_list.append(i.case_id)
                result_case = Case.objects.filter(case_id__in=id_list ).all()
                num_case = len(id_list)
                result_case, num_pages = calPage(result_case,page)
                case_types = Case_Type.objects.filter(case_id__in=id_list ).all()
                case_fields = Case_Field.objects.filter(case_id__in=id_list ).all()
                case_photo = CasePhoto.objects.filter(case_id__in=id_list ).all()
                query_list = id_list
                print("id_list",id_list,"\n")

                return render(request,'case/search.html',locals()) 
        
        # == 複合查詢判斷 ==
        else:
            print("Compound search  :" ,type ,field,num,date_time,work,constraint,location,con)

            # === 複合查詢判斷 - type =====
            temp_id_list =[]
            for i in type:
                # print("i:",i)
                temp_types = Case_Type.objects.filter(case_type= i).all()
                for j in temp_types:
                    temp_id_list.append(j.case_id) 
            print("temp_id_list: " , temp_id_list)

            # === 複合查詢判斷 - field =====
            for i in field:
                temp_types = Case_Field.objects.filter(case_field= i).all()
                for j in temp_types:
                    temp_id_list.append(j.case_id) 
            print("temp_id_list: " , temp_id_list)

            # === 複合查詢判斷 - other訊息
            temp = []  # 個別case值
            temp2 = [] # 存成list
            check_list = [] # 0代表無值; 1代表有值
            temp2_id_list =[] #用來紀錄交集其他5個選項

            ## 人數
            if num == 0:
                check_list.append(0)
                temp2.append(0)
            else:
                temp_case = Case.objects.filter(Q(num__lte=num) & Q(shown_public=True))
                for i in temp_case:
                    temp.append(i.case_id)
                temp2.append(temp)
                check_list.append(1)
            print("num_temp:",temp2)
              
            ## 日期
            if date_time == "2000-01-01":
                check_list.append(0)
                temp2.append(0)
            else:
                temp_case = Case.objects.filter( Q(ended_datetime__date__lte = date_time)& Q(shown_public=True))
                for i in temp_case:
                    temp.append(i.case_id)
                temp2.append(temp)
                check_list.append(1)
            print("date_temp:",temp2)
                
            ## 工作
            if  work == 100000000000000000:
                check_list.append(0)
                temp2.append(0)
            else:
                temp_case = Case.objects.filter( Q(work=work) & Q(shown_public=True))
                for i in temp_case:
                    temp.append(i.case_id)
                temp2.append(temp)
                check_list.append(1)
            print("work_temp:",temp2)

            ## 偏好
            if  constraint == "None":
                check_list.append(0)
                temp2.append(0)
            else:
                temp_case = Case.objects.filter( Q(constraint__icontains=constraint) & Q(shown_public=True))
                for i in temp_case:
                    temp.append(i.case_id)
                temp2.append(temp)
                check_list.append(1)
            print("constraint_temp:",temp2)

            ## 地點
            if  location == "None":
                check_list.append(0)
                temp2.append(0)
            else:
                temp_case = Case.objects.filter( Q(location__icontains=location)  & Q(shown_public=True))
                for i in temp_case:
                    temp.append(i.case_id)
                temp2.append(temp)
                check_list.append(1)
            print("location_temp:",temp2)

            record = []
            print("check_list:",check_list)
            # 交集複合搜尋的其他選項
            for i in range(5):
                if check_list[i] == 1:
                    record.append(i)
            print("record: ",record)

            if len(record) !=0 :
                for i in range(len(record)):
                    num = record[i]
                    #print(i)
                    if i == 0 :
                        temp2_id_list = temp2[num]
                        #print("temp2_id_list:",temp2_id_list)
                        #print("temp2[i]:",temp2[num])
                    else:
                        temp2_id_list = list(set(temp2_id_list) & set(temp2[num]))

            print("temp2_id_list:",temp2_id_list)

            # === 複合查詢id結果 - 交集類型/類型
            if con == "1": 
                
                # 若其他5個選項空值，應該直接輸出type 和 field的結果
                if check2 == 5:

                    # 關鍵字結果與type 和 field的交集結果
                    if query_list[0] != ''  :
                        id_list = []
                        id_list = list(set(temp_id_list)  & set(query_list))
                        print("其他五個選項沒有輸入，關鍵字結果與type 和 field的交集結果:",id_list)

                        result_case = Case.objects.filter(case_id__in=id_list ).all()
                        num_case = len(id_list)
                        result_case , num_pages = calPage(result_case,page)
                        case_types = Case_Type.objects.filter(case_id__in=id_list ).all()
                        case_photo = CasePhoto.objects.filter(case_id__in=id_list ).all()
                        case_fields = Case_Field.objects.filter(case_id__in=id_list ).all()
                        return render(request,'case/search.html',locals())
                    
                    else:
                        id_list = temp_id_list
                        print("其他五個選項沒有輸入，type 和 field的聯集結果:",id_list)
                        result_case = Case.objects.filter(case_id__in=id_list ).all()
                        num_case = len(id_list)
                        result_case, num_pages = calPage(result_case,page)
                        case_types = Case_Type.objects.filter(case_id__in=id_list ).all()
                        case_photo = CasePhoto.objects.filter(case_id__in=id_list ).all()
                        case_fields = Case_Field.objects.filter(case_id__in=id_list ).all()

                        return render(request,'case/search.html',locals()) 

                # 若其他5個選項有交集出結果，則繼續和 type 和 field的結果進行交集
                else:
                    id_list = list(set(temp_id_list)  & set(temp2_id_list))
                   
                    # === 複合查詢id結果 - 交集類型/類型/關鍵字
                    if  query_list[0] != '' :
                        query_id_list = []
                        query_id_list = list(set(id_list)  & set(query_list))
                        print("和其他5個選項 交集 關鍵字 與 type 和 field的結果 " ,query_id_list)
                        result_case = Case.objects.filter(case_id__in=query_id_list ).all()
                        num_case = len(query_id_list)
                        result_case , num_pages= calPage(result_case,page)
                        case_types = Case_Type.objects.filter(case_id__in=query_id_list ).all()
                        case_photo = CasePhoto.objects.filter(case_id__in=query_id_list ).all()
                        case_fields = Case_Field.objects.filter(case_id__in=query_id_list ).all()
                        return render(request,'case/search.html',locals())

                    print("和其他5個選項 交集 type 和 field的結果 id_list:" ,id_list)
                    result_case = Case.objects.filter(case_id__in=id_list ).all()
                    num_case = len(id_list)
                    result_case, num_pages = calPage(result_case,page)
                    case_types = Case_Type.objects.filter(case_id__in=id_list ).all()
                    case_photo = CasePhoto.objects.filter(case_id__in=id_list ).all()
                    case_fields = Case_Field.objects.filter(case_id__in=id_list ).all()

                    return render(request,'case/search.html',locals())
            

            else: 
                # 使用者未輸入任何資訊在進階搜尋時
                if check == 7:
                    alert = True
                    erro =json.dumps("請輸入搜尋條件")
                    result_case = Case.objects.filter(shown_public=True)
                    num_case = Case.objects.filter(shown_public=True).count()
                    result_case , num_pages= calPage(result_case,page)
                    case_fields = Case_Field.objects.all()
                    case_types = Case_Type.objects.all()
                    case_photo = CasePhoto.objects.all()
                    return render(request,'case/search.html',locals()) 

                
                # === 複合查詢id結果 -關鍵字與其他五個選項交集
                if query_list[0] != ''  :
                    id_list = []
                    id_list = list(set(temp2_id_list)  & set(query_list))
                    print("其他五個選項與關鍵字交集結果:",id_list)

                    result_case = Case.objects.filter(case_id__in=id_list ).all()
                    num_case = len(id_list)
                    result_case, num_pages = calPage(result_case,page)
                    case_types = Case_Type.objects.filter(case_id__in=id_list ).all()
                    case_photo = CasePhoto.objects.filter(case_id__in=id_list ).all()
                    case_fields = Case_Field.objects.filter(case_id__in=id_list ).all()
                    return render(request,'case/search.html',locals())
                
                # === 其他五個選項交集結果
                else:
                    id_list = temp2_id_list
                    print("其他五個選項相互交集結果:",id_list)
                    result_case = Case.objects.filter(case_id__in=id_list ).all()
                    num_case = len(id_list)
                    result_case , num_pages= calPage(result_case,page)
                    case_types = Case_Type.objects.filter(case_id__in=id_list ).all()
                    case_photo = CasePhoto.objects.filter(case_id__in=id_list ).all()
                    case_fields = Case_Field.objects.filter(case_id__in=id_list ).all()

                    return render(request,'case/search.html',locals()) 

    # 預設畫面，代所有case
    page_all = request.GET.get('page_all', 1)
    result_case = Case.objects.filter(shown_public=True)
    num_case = Case.objects.filter(shown_public=True).count()
    result_case, num_pages = calPage_index(result_case,page_all)
    case_fields = Case_Field.objects.all()
    case_types = Case_Type.objects.all()
    case_photo = CasePhoto.objects.all()

    return render(request,'case/search.html',locals()) 






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
                            oldUrl = os.path.join(settings.BASE_DIR, oldUrl)
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
def register(request):
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
        except:
            messages.warning(request,'信箱格式錯誤或已註冊')
            return redirect('register')

        # insert user detail into User
        user = User.objects.create_user(username=username, password=password, email=account, is_active=False)
        user.save()

        # insert user detail into UserDetail
        userDetail = UserDetail.objects.create(name=username, django_user=user, account_mail=account, salt=password)
        userDetail.save()

        request.session['messages'] = "請查看信箱點擊連結以完成註冊驗證。\n連結有效期為1個小時。"
        return HttpResponseRedirect('/')

    return render(request, 'register.html', locals())

# ------------email verification-------------
def active(request, token):
    # timeout
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        user = User.objects.get(Q(username=username))
        userDetail = UserDetail.objects.get(Q(django_user=user))
        userDetail.delete()
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

    return render(request, 'reset_pwd.html', locals())

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
