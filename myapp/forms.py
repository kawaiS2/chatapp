from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "image")

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

class NameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']
        widgets = {
                'username': forms.TextInput(attrs={'class': 'form-control'}),
            }

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']
        widgets = {
                'emaail': forms.TextInput(attrs={'class': 'form-control'}),
            }

class password_change(UserChangeForm):
    password = None
    model = CustomUser
    fields = ('password')

class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image']
        widgets = {
                'image': forms.FileInput(attrs={'class': 'form-control'}),
            }
