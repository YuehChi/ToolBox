from django.shortcuts import render
from .models import Status,Case,CasePhoto,Type,Case_Type,Field,Case_Field

# Create your views here.
def index(request):
   
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,'index.html',context={'num_visits': num_visits},
    )




# #### CASE ######
# #======新增CASE============
def case_new(request):

    ### 登入權限判斷
    if not request.user.is_authenticated:
       return render(request,'index.html')
    
    else:


        context ={

        }

        return render(request,'case/new.html',context=context)

# #======詳細CASE資訊============
def case_profile(request):

    context ={

    }

    return render(request,'case/profile.html',context=context)


# #======編輯CASE資訊============
def case_profile_edit(request):

    context ={

    }

    return render(request,'case/profile_edit.html',context=context)

# #======CASE資訊搜尋============
def case_search(request):

    context ={

    }
    return render(request,'case/search.html',context=context)

