from django.forms import forms

from .models import SubmissionFile

class UploadFileForm(forms.ModelForm):
    
    class Meta:
        model = SubmissionFile
        fields = ("",)
