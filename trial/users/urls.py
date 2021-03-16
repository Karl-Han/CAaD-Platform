from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path(r'', views.LoginView.as_view(), name='login'),
    path(r'logout/', views.logout_view, name='logout_view'),
    path(r'signup/', views.SignupView.as_view(), name='signup'),
    path(r'profile/<str:username>', views.profile, name='profile'),
]
