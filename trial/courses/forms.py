from django import forms
from .models import Course
from courses.utils import getRandCPwd

class CourseForm(forms.ModelForm):
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
        super(CourseForm, self).__init__(*args, **kwargs)