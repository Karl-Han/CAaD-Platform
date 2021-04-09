from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, View
from django.views.generic.base import ContextMixin
from django.contrib import messages

from users.models import User
from courses.models import Course, CourseMember
from utils.general import info, get_referer
from .models import SubmissionFile
from .forms import UploadFileForm

class TestUploadFileFormView(View, ContextMixin):
    template_name = "files/upload.html"
    extra_context = {"title": "Submission File upload"}

    def get(self, request):
        context = super().get_context_data()
        context['form'] = UploadFileForm()
        request.session['referer'] = get_referer(request)
        return render(request, self.template_name, context)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            messages.info(request, "Successfully upload file.")
            return redirect(request.session['referer'])
        context = super().get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

def downloadFile(request, file_id):
    return SubmissionFile.get_file_response(file_id)

def deleteFile(request, file_id):
    file = get_object_or_404(SubmissionFile, pk=file_id)
    file.delete()
    return info(request, "Successfully deleted {}".format(file_id))