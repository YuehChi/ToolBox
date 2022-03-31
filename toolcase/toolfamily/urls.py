from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout),
    path('register/', views.register),
    path('activate/<str:token>', views.active),
    path('forget/', views.forget),
    path('reset/<str:token>', views.reset),
    path('home/', views.index, name='index'),
]

# urlpatterns += [
# ]