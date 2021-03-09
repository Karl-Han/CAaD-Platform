from django.urls import path

from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('create', views.CreatecourseView.as_view(), name='create'),
    path('<int:course_id>', views.coursePage, name='homepage'),
    path('<int:pk>/edit', views.EditcourseView.as_view(), name='edit'),
    path('<int:course_id>/join', views.joinCourse, name='join'),

    # TODOs
    # path('<int:course_id>/students', views.manageStudents, name='manage_students'),
    # path('<int:course_id>/task', views.manageTasks, name='manage_tasks'),
    # path('<int:course_id>/announcements', views.manageAnnounce, name='manage_announces'),
]
