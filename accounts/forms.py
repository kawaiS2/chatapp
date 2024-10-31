from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomSignUpForm(SignupForm):
    image = forms.ImageField(required=False)

    def save(self,request):
        user = super(CustomSignUpForm, self).save(request)
        user.image = self.cleaned_data.get('image')
        user.save()
        return user