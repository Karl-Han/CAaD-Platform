from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('doSignup', views.doSignup, name='doSignup'),
    path('login', views.login, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('<str:ownerName>', views.profile, name='profile'),
]
