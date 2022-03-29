from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]



## Case urls
urlpatterns += [
    path('case/',views.index, name='index'),
    path('case/new/',views.case_new, name='case-new'),
    path('case/profile/<int:case_id>/', views.case_profile, name='case-profile' ),
    path('case/profile/<int:case_id>/edit/',views.case_profile_edit, name='case-profile-edit'),
    path('case/search/', views.case_search,name='case-search'),
]


