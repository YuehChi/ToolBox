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
]
