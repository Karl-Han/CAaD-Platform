from django.urls import path

from . import views

app_name = 'homeworks'
urlpatterns = [
    path('', views.index, name='index'),
    path('doCreate', views.doCreate, name='docreate'),
    path('<int:hid>', views.getHomework, name='getHomework')
]
