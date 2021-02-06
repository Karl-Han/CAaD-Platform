from django.urls import path

from . import views

app_name = 'homeworks'
urlpatterns = [
    path('', views.index, name='index'),
    path('doCreate', views.doCreate, name='docreate'),
    path('commitments/<int:hsid>', views.getHomeworkStatu, name='getHomeworkStatu'),
    path('<int:hid>', views.getHomework, name='getHomework'),
    path('<int:hid>/commit', views.commitHomework, name='commitHomework')
]
