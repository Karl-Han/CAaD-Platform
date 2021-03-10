from django.urls import path

from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('create', views.CreatecourseView.as_view(), name='create'),
    path('<int:course_id>', views.homepage, name='homepage'),
    path('<int:pk>/edit', views.EditcourseView.as_view(), name='edit'),
    path('<int:course_id>/join', views.joinCourse, name='join'),

    # TODOs
    path('<int:course_id>/students', views.StudentsListView.as_view(), name='manage_students'),
    path('changePrivilege/<int:member_record>', views.ChangePrivilegeView.as_view(), name='change_privilege'),
    # path('<int:course_id>/task', views.manageTasks, name='manage_tasks'),
    # path('<int:course_id>/announcements', views.manageAnnounce, name='manage_announces'),
]
