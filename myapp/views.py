from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import UserRegistrationForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from  .forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)  # ユーザーを自動的にログインさせる
            return redirect('index')  # リダイレクト先のページを設定
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()

    return render(request, 'myapp/signup.html', {'user_form': user_form, 'profile_form': profile_form})

def login_view(request):
    return render(request, "myapp/login.html")

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = '/login/'
    
class Login(LoginView):
    template_name = 'login.html'
    form_class = LoginForm

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
