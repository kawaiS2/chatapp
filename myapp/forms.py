from django import forms
from accounts.models import CustomUser
from django.contrib.auth.forms import UserChangeForm

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
