from django.urls import path

from . import views

app_name = 'homeworks'
urlpatterns = [
    path('<int:course_id>', views.TaskListView.as_view(), name='task_list'),
    path('task/<int:task_id>', views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:course_id>/createTask', views.CreateTaskView.as_view(), name='create_task'),
    path('task/<int:task_id>/submissions', views.SubmissionListView.as_view(), name='submission_list'),
    path('submission/<int:pk>/comment', views.SubmissionCommentUpdateView.as_view(), name='submission_comment'),
]
