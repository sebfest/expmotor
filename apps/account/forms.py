from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'

    first_name = forms.CharField(help_text='This name will appear in emails sent to participants.')
    last_name = forms.CharField(help_text='This name will appear in emails sent to participants.')
    email = forms.EmailField(help_text='An activation link will be sent to this email address.')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
