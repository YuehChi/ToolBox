from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]




#####################################
#           CASE URLS               #
#####################################
urlpatterns += [
    path('case/',views.index, name='index'),
    path('case/new/',views.case_new, name='case-new'),
    path('case/profile/<int:case_id>/', views.case_profile, name='case-profile' ),
    path('case/profile/<int:case_id>/edit/',views.case_profile_edit, name='case-profile-edit'),
    path('case/search/', views.case_search,name='case-search'),
    #### use temp url
    path('case/new_temp/',views.case_new_temp, name='new_temp'),
    path('case/case_all_temp/',views.case_all_temp, name='case_all_temp'),
]


