from django import forms
from django.forms import modelformset_factory
from .models import Course, CourseMember
from courses.utils import getRandCPwd

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
    
class JoinForm(forms.Form):
    password = forms.CharField(max_length=8)

class ManageStudentForm(forms.ModelForm):
    class Meta:
        model = CourseMember
        fields = ("course", "user", "type")
        widgets = {
            # 'user.username': forms.TextInput(attrs={'disabled': True}),
        }
    def __init__(self, *args, **kwargs):
        self.course_id = kwargs.pop("course_id")
        super(ManageStudentForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(pk=self.course_id)

BaseManageStudentFormSet = modelformset_factory(CourseMember, form=ManageStudentForm, can_delete=True)

class ManageStudentFormSet(BaseManageStudentFormSet):
    def __init__(self, *args, **kwargs):
        self.course_id = kwargs.pop("course_id")
        super(ManageStudentFormSet, self).__init__(*args, **kwargs)
    
    def _construct_form(self, *args, **kwargs):
        # Call this function before getting form
        # Pass course_id to ManasgeStudentForm
        kwargs['course_id'] = self.course_id
        return super(ManageStudentFormSet, self)._construct_form(*args, **kwargs)