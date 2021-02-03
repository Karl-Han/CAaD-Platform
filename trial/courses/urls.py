from django.urls import path

from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.createCourse, name='create'),
    path('doCreate', views.doCreate, name='doCreate'),
    path('<str:cname>', views.coursePage, name='coursePage'),
    path('<str:cname>/join', views.doJoin, name='doJoin'),
    path('<str:cname>/newpwd', views.doChangePwd, name='doChangePwd'),
    path('<str:cname>/<str:uname>/del', views.doDelUser, name='doDelUser'),
]
