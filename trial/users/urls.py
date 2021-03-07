from django.urls import path
# from django.contrib.auth.views import LoginView

from . import views
from .views import SignupView, LoginView
from trial.views import index

app_name = 'users'
urlpatterns = [
    path(r'', LoginView.as_view(), name='login'),
    path(r'signup/', SignupView.as_view(), name='signup'),
    path(r'login/', LoginView.as_view(), name='login'),
    path(r'profile/<str:username>', views.profile, name='profile'),
]
