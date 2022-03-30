from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login.html'),
    path('logout/', views.logout),
    path('home/', views.index, name='index'),
]

# urlpatterns += [
# ]