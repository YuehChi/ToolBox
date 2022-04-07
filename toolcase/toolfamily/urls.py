from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]





#####################################
#           USER URLS               #
#####################################
urlpatterns += [
    path('user/profile/', views.viewUser, name='user-profile'),
    path('user/profile/update/', views.updateUser, name='user-profile-update'),
    path('user/icon/update/', views.updateUserIcon, name='user-icon-update'),
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
]


