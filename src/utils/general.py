from django.shortcuts import render
from django.template.loader import render_to_string

from utils.status import *
from courses.models import CourseMember

def get_referer(request):
    return request.META.get('HTTP_REFERER')

def return_error(request, error_id):
    return render(request, "generics/error.html", { "error_id": error_id, "error_msg": ERROR_LIST[error_id], "redirect_to": get_referer(request) })

def error_not_authenticated(request):
    return return_error(request, USER_NOT_AUTHENTICATED)

def info(request, msg, redirect_to=None):
    """
    Display message and redirect

    Input:
        * request
        * msg: message to display
        * redirect_to=None: jump to next page
    Output:
        * HttpResponse with `generics/info.html`
    """
    context = {}
    context['previous'] = get_referer(request)
    context['msg'] = msg

    if redirect_to:
        context['redirect_to'] = redirect_to
    
    return render(request, "generics/info.html", context)

def check_authenticated_and(request, criteria=None, error_code=None):
    """
    Check request authenticated and criteria

    Input:
        * request
        * criteria=None: True or False
        * error_code: error when criteria is False
    Output: (res, response)
        * res: request.is_authenticated and criteria
        * response: if not res, then error response
    """
    if not request.user.is_authenticated:
        return (False, return_error(request, USER_NOT_AUTHENTICATED))
    if criteria is not None and not criteria:
        return (False, return_error(request, error_code))
    return (True, None)

def get_navigation(user):
    try:
        privilege = CourseMember.get_highest_privilege(user.pk)
        # User privilege: navi content
        # 4(Not even student): Homepage
        # 3(Student): My Courses, My Tasks, My Submissions
        # 2(TA): Student + Teaching
        # 1(Teacher): TA + Background
        # 0(Course Admin): Teacher

        # list(dict(name, url))
        navi_list = []
        if privilege <= 3:
            pass
            if privilege <= 2:
                if privilege <= 1:
                    if privilege == 0:
                        pass
        else:
            # 4 or something else
            pass
        return render_to_string("generics/navi.html", {"navi_list": navi_list})
    except Exception as e:
        print(e)
        return ""