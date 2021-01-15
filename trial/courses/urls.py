from django.urls import path

from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.createCourse, name='create'),
    path('doCreate', views.doCreate, name='doCreate'),
    path('<str:cname>', views.coursePage, name='coursePage'),
    path('<str:cname>/join', views.doJoin, name='doJoin'),
]
