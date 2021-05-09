from django.urls import path

from . import views, views_my
import homeworks.views as homework_views

app_name = 'courses'
urlpatterns = [
    # Basic operation
    # path('', views.PlatformHomepageView.as_view(), name='index'),
    path('create', views.CreateCourseView.as_view(), name='course_create'),
    path('<int:course_id>', views.course_homepage, name='course_homepage'),
    path('<int:pk>/edit', views.EditcourseView.as_view(), name='course_edit'),
    path('<int:course_id>/join', views.joinCourse, name='course_join'),

    # My* Views
    path('myTeaching', views_my.MyTeachingCourseListView.as_view(), name='teaching_list_my'),
    path('myStudying', views_my.MyStudyingCourseListView.as_view(), name='studying_list_my'),
    path('myTasks', views_my.MyTasksListView.as_view(), name='tasks_list_my'),

    # Member management
    path('<int:course_id>/students', views.StudentsListView.as_view(), name='students_manage'),
    path('changePrivilege/<int:member_record>', views.ChangePrivilegeView.as_view(), name='privilege_change'),

    # Task handling 
    path('<int:course_id>/tasks', homework_views.TaskListView.as_view(), name='task_list'),
    path('<int:course_id>/createTask', homework_views.CreateTaskView.as_view(), name='task_create'),
    path('task/<int:task_id>', homework_views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/update', homework_views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:task_id>/submissions', homework_views.SubmissionListView.as_view(), name='submission_list'),
    path('submission/<int:pk>/comment', homework_views.SubmissionCommentUpdateView.as_view(), name='submission_comment'),

    # TODOs
    # path('<int:course_id>/announcements', views.manageAnnounce, name='manage_announces'),
]
