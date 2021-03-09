from django import forms
from .models import Course
from courses.utils import getRandCPwd

# class EditCourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ('name', 'password', 'description', 'is_open')

class CreateCourseForm(forms.ModelForm):
    password = forms.CharField(max_length=8, required=False)

    def clean_password(self):
        p = self.cleaned_data['password']
        if p == '':
            return getRandCPwd()
        return p

    class Meta:
        model = Course
        fields = ('name', 'password', 'description')

    def __init__(self, *args, **kwargs):
        creator = kwargs.get("creator")
        if creator:
            print(creator)
            kwargs.pop("creator")
            self.creator = creator
        else:
            print("No Creator")
        super(CreateCourseForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.creator = self.creator
        course = super(CreateCourseForm, self).save(*args, **kwargs)
        return course