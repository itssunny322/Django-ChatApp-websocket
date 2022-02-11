from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

class SignUpForms(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        help_texts = {'password1':('sunny')}

class LoginForms(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
            )

