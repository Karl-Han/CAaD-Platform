from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views import View
from django.contrib import messages

from courses.models import Course, CourseMember
from .models import User
from .forms import UserForm, LoginForm

from .utils import get_enrolled_courses

class SignupView(View):
    template_name = 'users/signup.html'

    def get(self, request):
        user = UserForm()
        context = {"form": user}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("users:login"))
        context = {'form': form}
        return render(request, self.template_name, context)

class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, message="Please first logout to login.")
            return redirect(reverse("users:profile", args=[request.user.username]))
        form = LoginForm()
        print(form)
        context = { "form": form }
        return render(request, self.template_name, context)

    def post(self, request):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # print(user)

        if user is None:
            # Not an authenticated user
            print("Not Authenticated from {}".format(request.POST['username']))
            context = { 'form': LoginForm(request.POST), 'error': "No such user or wrong password"}
            return render(request, self.template_name, context=context)
        login(request, user)

        # return render(request, 'users/info.html', {'info': "Successfully login"})
        messages.info(request, "Successfully login")
        return redirect(request.META['HTTP_REFERER'])

def profile(request, username):
    owner = get_object_or_404(User, username=username)
    context = {}

    # Get login user
    # * if user_id == user.pk -> print self profile + enrolled courses
    # * not equal -> print open profile
    print(owner)
    if request.user.is_authenticated and request.user.pk == owner.pk:
        context["course_info_list"] = get_enrolled_courses(request.user)
    else:
        context["others_name"] = owner.get_username()

    print(context)
    return render(request, 'users/profile.html', context)

def logout_view(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])