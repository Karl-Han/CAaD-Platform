from django.urls import path

from . import views

app_name = 'files'
urlpatterns = [
    # path('', views.FileCreateView.as_view(), name='index'),
    path('', views.TestUploadFileFormView.as_view(), name='index'),
    path('download/<int:file_id>', views.downloadFile, name='download'),
    path('delete/<int:file_id>', views.deleteFile, name='delete'),
]