from django import forms
from django.forms import ModelForm, Form

from .models import SubmissionFile

class UploadFileForm(ModelForm):
    class Meta:
        model = SubmissionFile
        fields = ("file",)

class UploadDockerfileForm(Form):
    file = forms.FileField(label="Zip Dockerfile", help_text="Root directory must include the Dockerfile")
    port_open = forms.IntegerField(min_value=0, max_value=65535, required=False, help_text="Enter open port of Dockerfile if needed.")

    def clean_file(self):
        file = self.cleaned_data['file']
        if file.content_type != "application/zip":
            raise forms.ValidationError("Wrong content type. It should be application/zip")

        return file