from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from courses.models import Course, CourseMember
from .models import UserAuxiliary
from .forms import UserForm, LoginForm, EditForm

from .utils import get_enrolled_courses

class SignupView(View):
    template_name = 'users/signup.html'

    def get_context_data(self, **kwargs):
        context = {}
        context["title"] = "Sign Up"
        return context

    def get(self, request):
        user = UserForm()
        context = self.get_context_data()
        context["form"] = user
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            obj = form.save()
            obj.auxiliary = UserAuxiliary(user=obj)
            obj.auxiliary.save()
            return HttpResponseRedirect(reverse("users:login"))

        context = self.get_context_data()
        context["form"] = form
        return render(request, self.template_name, context)

class LoginView(View):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = {}
        context["title"] = "Login"
        return context

    def get(self, request):
        context = self.get_context_data()
        form = LoginForm()

        if request.user.is_authenticated:
            messages.info(request, message="Please first logout to login.")
            return redirect(reverse("users:profile", args=[request.user.username]))

        context["form"] = form
        context["title"] = "Login"
        return render(request, self.template_name, context)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            messages.info(request, "Successfully login")
            return redirect(request.META['HTTP_REFERER'])

        return render(request, self.template_name, {"form": form})

def profile(request, username):
    owner = get_object_or_404(User, username=username)
    context = {}
    context['title'] = "User Profile"

    # Get login user
    # * if user_id == user.pk -> print self profile + enrolled courses
    # * not equal -> print open profile
    # print(owner)
    if request.user != owner:
        context["others_name"] = owner.get_username()
    else:
        context["course_info_list"] = get_enrolled_courses(request.user)
        context["owner"] = owner
        context["owner_aux"] = owner.auxiliary

    return render(request, 'users/profile.html', context)

def logout_view(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])

class EditUserInfo(View):
    template_name = "users/edit.html"

    def get_context_data(self, **kwargs):
        context = {}
        context["title"] = "Edit User Info"
        return context
    
    def get(self, request, user_id):
        # Do authentication elsewhere
        context = self.get_context_data()

        user = request.user
        form = EditForm(initial={'email': user.email, 'realname': user.auxiliary.realname, 'uid': user.auxiliary.uid})
        context["form"] = form

        return render(request, self.template_name, context)

    def post(self, request, user_id):
        # Do authentication elsewhere
        context = self.get_context_data()
        form = EditForm(request.POST)

        if form.is_valid():
            if user_id == request.user.pk:
                user = request.user
                data = form.cleaned_data

                user.email = data['email']
                user.auxiliary.realname = data['realname']
                user.auxiliary.uid = data['uid']

                user.save()
                user.auxiliary.save()
                messages.info(request, "Successfully update")
                return redirect(reverse("users:profile", args=[user.username]))
        context['form'] = form

        return render(request, self.template_name, context)