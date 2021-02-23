from django import forms
from django.core.exceptions import ValidationError

from .models import User


class UserForm(forms.ModelForm):
    # No need for a clean_email because it has already been 
    # clean by the Validator
    # def clean_email():

    class Meta:
        model = User
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        fields = (
            'nickname', 'password', 'email', 
            'uid', 'realname'
        )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # self.fields['uid'].required = False
        # self.fields['realname'].required = False

    # # Clean fields: nickname, email
    # def clean_nickname(self):
    #     u = User.objects.filter(nickname=self.nickname)
    #     if u.exists():
    #         raise 
