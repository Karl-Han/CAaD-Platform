from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, View
from django.contrib import messages

from users.models import User
from courses.models import Course, CourseMember
# from homeworks.models import Homework, HomeworkStatu
from .models import SubmissionFile#, FileHomeworkStatu
from .forms import UploadFileForm

import json

from utils.check import info, checkReqData, checkUser
from utils.status import *
from utils.parms import HW_FILE_LIMIT, HS_FILE_LIMIT

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

# def uploadHomeworkFile(request):
#     if request.method != 'POST':
#         raise PermissionDenied
# 
#     crd_st, rd = checkReqData(request, post=['hid'], files=['hfile'])
#     if crd_st == -1:
#         return rd
#     try:
#         hid = int(request.POST['hid'])
#     except:
#         return info(request, INFO_HACKER)
# 
#     cu_st, tmp = checkUser(request)
#     if not cu_st == 1:
#         return tmp
#     user = tmp
# 
#     # check cm
#     try:
#         h = Homework.objects.get(pk=hid)
#         c = Course.objects.get(pk=h.cid)
#         cm = CourseMember.objects.get(cid=c.pk, uid=user.pk)
#     except:
#         return info(request, INFO_HACKER)
#     if cm.types >= 3:
#         return info(request, INFO_HACKER)
# 
#     # limit
#     fhs = FileHomework.objects.filter(hid=hid)
#     if len(fhs) >= HW_FILE_LIMIT:
#         return info(request, INFO_LIMIT, INFO_STR[INFO_LIMIT]%('Homework file', HW_FILE_LIMIT))
# 
#     # save
#     try:
#         fh = FileHomework(
#             uid = user.pk,
#             create_date = timezone.now(),
#             hid = h.pk,
#             file = request.FILES['hfile']
#         )
#         fh.save()
#     except:
#         return info(request, INFO_DB_ERR)
# 
#     return info(request, SUCCESS)
# 
# 
