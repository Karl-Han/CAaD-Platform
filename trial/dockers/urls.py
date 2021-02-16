from django.urls import path

from . import views

app_name = 'dockers'
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.createDocker, name='createDocker'),
    path('delete', views.deleteDocker, name='deleteDocker'),
]
