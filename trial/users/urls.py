from django.urls import path

from . import views
from .views import SignupView

app_name = 'users'
urlpatterns = [
    path(r'', views.index, name='user_index'),
    path(r'signup', SignupView.as_view(), name='signup'),
    # path(r'doSignup', views.doSignup, name='doSignup'),
    path(r'login', views.login, name='login'),
    path(r'doLogin', views.doLogin, name='doLogin'),
    path(r'getUC', views.getUC, name='getUC'),
    path(r'profile/<str:ownerName>', views.profile, name='profile'),
]
