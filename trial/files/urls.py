from django.urls import path

from . import views

app_name = 'files'
urlpatterns = [
    path('', views.FileCreateView.as_view(), name='index'),
    # path('upload/hw', views.uploadHomeworkFile, name='uploadHomeworkFile'),
]
