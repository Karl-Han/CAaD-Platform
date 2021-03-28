from django.urls import path

from . import views

app_name = 'dockers'
urlpatterns = [
    path('<int:task_id>/uploadDockerfile', views.UploadDockerfileView.as_view(), name='dockerfile_upload'),
    # path('image/<int:dockerfile_id>', views.DockerfileDetailView, name='dockerfile_view'),
    # path('review', views.ReviewDockerListView.as_view(), name='dockerfile_review'),
    path('<int:submission_id>/containerStatus', views.containerStatus, name='container_status'),
    # path('<int:submission_id>', views.index, name='container_list'),
    path('<int:submission_id>/createContainer', views.createContainer, name='container_create'),
    path('<int:submission_id>/deleteContainer', views.deleteContainer, name='container_delete'),
]
