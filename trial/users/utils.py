from courses.models import CourseMember
from courses.utils import COURSEMEMBER_TYPE

def get_enrolled_courses(user):
    enrolled_courses = CourseMember.objects.filter(user=user)
    course_info_list = []
    for role in enrolled_courses:
        course = role.course
        course_info_list.append({
            'name': course.name,
            'id': course.pk,
            'role': COURSEMEMBER_TYPE[role.type]
        })
    return course_info_list 
