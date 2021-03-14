from django.forms import ModelForm 

from .models import SubmissionFile

class UploadFileForm(ModelForm):
    class Meta:
        model = SubmissionFile
        fields = ("file",)
