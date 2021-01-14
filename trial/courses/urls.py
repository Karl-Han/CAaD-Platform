from django.urls import path

from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('createCourse', views.createCourse, name='createCourse'),
    path('doCreate', views.doCreate, name='doCreate'),
    path('<str:cname>', views.coursePage, name='coursePage'),
]
