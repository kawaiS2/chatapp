from django.shortcuts import redirect, render, get_object_or_404
from .forms import LoginForm, SignUpForm, NameChangeForm, EmailChangeForm, ImageChangeForm
from .models import ChatRoom, Message
from django.shortcuts import render
from django.contrib.auth import get_user_model
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
    
class login_view(LoginView):
    template_name = 'myapp/login.html'
    form_class = LoginForm

User = get_user_model()

@login_required
def friends(request):
    users = User.objects.exclude(id=request.user.id)
    user_data = []

    for user in users:
        # ルームを取得（存在しない場合はNone）
        room = ChatRoom.objects.filter(
            user1=min(request.user, user, key=lambda u: u.id),
            user2=max(request.user, user, key=lambda u: u.id)
        ).first()

        last_message = room.messages.order_by('-timestamp').first() if room else None

        user_data.append({
            'user': user,
            'last_message': last_message.content if last_message else '',
            'timestamp': last_message.timestamp if last_message else None,
        })

    return render(request, 'myapp/friends.html', {'user_data': user_data})

@login_required
def talk_room(request, user_id):
    user2 = get_object_or_404(User, id=user_id)
    
    room, created = ChatRoom.objects.get_or_create(
        user1=min(request.user, user2, key=lambda u: u.id),
        user2=max(request.user, user2, key=lambda u: u.id)
    )

    messages = room.messages.order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(room=room, sender=request.user, content=content)
        return redirect('talk_room', user_id=user2.id)

    return render(request, 'myapp/talk_room.html', {'room': room, 'messages': messages, 'user2': user2})

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