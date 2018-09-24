from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('is_dev',)


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='Username',
                               required=True,
                               max_length=100,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'name': 'username',
                                       'placeholder': 'Enter Username'
                                   }
                               ))
    password = forms.CharField(label='Password',
                               required=True,
                               max_length=100,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'name': 'password',
                                       'placeholder': 'Enter Password',
                                       'type': 'password'
                                   }
                               ))


class RegistrationForm(forms.Form):
    name = forms.CharField(label='Your Name',
                           required=False,
                           max_length=100,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'name': 'name',
                                   'placeholder': 'Enter Your Name'
                               }
                           ))
    email = forms.CharField(label='Your Email',
                            required=True,
                            max_length=100,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'name': 'email',
                                    'placeholder': 'Enter Your Email'
                                }
                            ))
    is_dev = forms.BooleanField(label='Are you a developer?',
                                initial=False,
                                required=False,
                                help_text='Check this if you are a developer or a game publisher.',
                                widget=forms.CheckboxInput(
                                    attrs={
                                        'name': 'is_dev'
                                    }
                                ))
    username = forms.CharField(label='Username',
                               required=True,
                               max_length=100,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'name': 'username',
                                       'placeholder': 'Enter Your Username'
                                   }
                               ))
    password = forms.CharField(label='Password',
                               required=True,
                               max_length=100,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'name': 'password',
                                       'placeholder': 'Enter Your Password',
                                       'type': 'password'
                                   }
                               ))
    confirmPassword = forms.CharField(label='Confirm Password',
                                      required=True,
                                      max_length=100,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control',
                                              'name': 'confirmPassword',
                                              'placeholder': 'Re-enter Your Password',
                                              'type': 'password'
                                          }
                                      ))
