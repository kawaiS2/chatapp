from django.shortcuts import redirect, render
from .forms import LoginForm, SignUpForm
from .models import CustomUser
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'myapp/signup.html', context)

def friends_list(request):
    friends = CustomUser.objects.all()  

    context = {
        'CustomUser': friends
    }
    return render(request, 'myapp/friends.html', context)
    
class login_view(LoginView):
    template_name = 'myapp/login.html'
    form_class = LoginForm

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
