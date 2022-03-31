from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout),
    path('register/', views.register),
    path('activate/<str:token>', views.active),
    path('forget/', views.forget, name='forget-pwd'),
    path('reset/', views.reset, name='reset-pwd'),
    path('home/', views.index, name='index'),
]

# urlpatterns += [
# ]