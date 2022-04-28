from django.urls import path
from . import views


#####################################
#           AUTH URLS               #
#####################################
urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register/check/', views.check_mail_used, name='check-mail-used'),
    path('activate/<str:token>/', views.active, name='active'),
    path('forget/', views.forget, name='forget'),
    path('reset/<str:token>/', views.reset, name='reset'),
    path('home/', views.index, name='index'),
]


#####################################
#           USER URLS               #
#####################################
urlpatterns += [
    path('user/profile/', views.viewUser, name='my-user-profile'),
    path('user/profile/<int:user_id>/', views.viewOtherUser, name='others-user-profile'),
    path('user/profile/update/', views.updateUser, name='user-profile-update'),
    path('user/icon/update/', views.updateUserIcon, name='user-icon-update'),
    path('user/password/update/', views.updatePassword, name='user-password-update'),
    path('user/publish/', views.user_publish_record, name='user-publish-record'),
    path('user/publish/<int:case_id>', views.user_publish_applicant, name='user-publish-applicant'),
    path('user/build/', views.build_commission, name='build-commission'),
    path('user/take/', views.user_take_record, name='user-take-record'),
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

#####################################
#           TAKE URLS               #
#####################################
urlpatterns += [
    path('user/cancel/<int:case_id>', views.user_cancel_willingess, name='user-cancel-willingess'),
    path('user/publish/', views.user_publish_record, name='user-publish-record'),
    path('user/publish/<int:case_id>', views.user_publish_applicant, name='user-publish-applicant'),
    path('user/take/', views.user_take_record, name='user-take-record'),
    path('user/build/', views.build_commission, name='build-commission'),
    path('user/delete/<int:commission_id>/', views.delete_commission, name='delete-commission'),
    path('user/finish/<int:commission_id>/', views.finish_commission, name='finish-commission'),
    path('user/rate/', views.rate, name='rate'),

    path('case/take/<int:case_id>',views.take_case, name='take-case'),
    path('case/cancel/<int:case_id>', views.cancel_willingess, name='cancel-willingess'),
]

#####################################
#           API URLS               #
#####################################
urlpatterns += [
    path('cases/', views.Case_list.as_view()),
    path('cases/<int:pk>', views.case_detail),
    path('reports/', views.ReportList.as_view()),
]
