from django.shortcuts import redirect, render
from .forms import LoginForm, SignUpForm, NameChangeForm, EmailChangeForm, ImageChangeForm
from .models import CustomUser
from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

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

@login_required
def name_change(request):
    if request.method == 'POST':
        form = NameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('setting')
    else:
        form = NameChangeForm(instance=request.user)
    return render(request, 'myapp/change_username.html', {'form': form})

@login_required
def email_change(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('setting')
    else:
        form = EmailChangeForm(instance=request.user)
    return render(request, 'myapp/change_email.html', {'form': form})

@login_required
def image_change(request):
    if request.method == 'POST':
        form = ImageChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('setting') 
    else:
        form = ImageChangeForm(instance=request.user)

    return render(request, 'myapp/change_image.html', {'form': form})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('setting')  
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'myapp/change_password.html', {'form': form})

class Logout(LogoutView):
    template_name = 'myapp/index.html'