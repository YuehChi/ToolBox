from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('activate/<str:token>', views.active, name='active'),
    path('forget/', views.forget, name='forget'),
    path('reset/<str:token>', views.reset, name='reset'),
    path('home/', views.index, name='index'),
]

# urlpatterns += [
# ]