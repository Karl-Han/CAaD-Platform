from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

# from .models import UserAuxiliary

class UserForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        fields = (
            'username', 'password1', 'password2', 'email' 
        )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data

        if data['password1'] != data['password2']:
            raise ValidationError("Two password not match")

        return data

class LoginForm(forms.Form):
    # email = forms.EmailField(label='email')
    username = forms.CharField(max_length=256)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])

        if user == None:
            raise ValidationError("No such user or wrong password")

        return data

class EditForm(forms.Form):
    realname = forms.CharField(max_length=16)
    uid = forms.CharField(max_length=32)
    email = forms.EmailField()