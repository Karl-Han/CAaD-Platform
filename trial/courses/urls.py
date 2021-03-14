from django.urls import path

from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='course_list'),
    path('create', views.CreatecourseView.as_view(), name='course_create'),
    path('<int:course_id>', views.homepage, name='course_homepage'),
    path('<int:pk>/edit', views.EditcourseView.as_view(), name='course_edit'),
    path('<int:course_id>/join', views.joinCourse, name='course_join'),

    # TODOs
    path('<int:course_id>/students', views.StudentsListView.as_view(), name='students_manage'),
    path('changePrivilege/<int:member_record>', views.ChangePrivilegeView.as_view(), name='privilege_change'),
    # path('<int:course_id>/task', views.manageTasks, name='manage_tasks'),
    # path('<int:course_id>/announcements', views.manageAnnounce, name='manage_announces'),
]
