from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect

def index(request):
    return render(request, "myapp/index.html")

class signup_view(CreateView):
    form_class = SignUpForm
    template_name = "myapp/signup.html"
    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())

class friends(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/friends.html'
    login_url = '/login/'
    
class login_view(LoginView):
    template_name = 'myapp/login.html'
    form_class = LoginForm

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
