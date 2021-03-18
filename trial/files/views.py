from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, View
from django.contrib import messages

from users.models import User
from courses.models import Course, CourseMember
from .models import SubmissionFile
from .forms import UploadFileForm

# # Create your views here.
class FileCreateView(CreateView):
    model = SubmissionFile
    fields = ["file"]
    template_name = "files/file_create.html"
    success_url = '/'

class TestUploadFileFormView(View):

    def get(self, request):
        form = UploadFileForm()
        return render(request, "files/file_create.html", { "form": form })

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            messages.info("Successfully upload file.")
        return render(request, "files/file_create.html", { "form": form })

def downloadFile(request, file_id):
    return SubmissionFile.get_file_response(file_id)

def deleteFile(request, file_id):
    file = get_object_or_404(SubmissionFile, pk=file_id)
    url = file.delete()
    file.save()
    return HttpResponse("Successfully deleted {}".format(file_id))