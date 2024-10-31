from django.shortcuts import redirect, render, get_object_or_404
from .forms import NameChangeForm, EmailChangeForm, ImageChangeForm
from .models import ChatRoom, Message
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.db.models import Q, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.utils import timezone


def index(request):
    return render(request, "myapp/index.html")

User = get_user_model()

from django.db.models import OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.db.models import Q

def friends(request):
    query = request.GET.get('q')
    if query:
        friends = CustomUser.objects.filter(
            Q(username__icontains=query)| Q(email__icontains=query)
        ).exclude(id=request.user.id).select_related()
    else:
        friends = CustomUser.objects.exclude(id=request.user.id).select_related()

    friends_ids = friends.values_list("pk", flat=True)

    rooms = ChatRoom.objects.filter(
        (Q(user1=request.user) & Q(user2__in=friends_ids)) |
        (Q(user2=request.user) & Q(user1__in=friends_ids))
    ).select_related('user1', 'user2') 
    
    latest_messages = Message.objects.filter(
        room=OuterRef('pk')
    ).order_by('-timestamp')

    rooms = rooms.annotate(
        latest_message_content=Subquery(latest_messages.values('content')[:1]),
        latest_message_timestamp=Coalesce(Subquery(latest_messages.values('timestamp')[:1]), timezone.now())
    )

    room_dict = {}
    for room in rooms:
        friend_id = room.user1_id if room.user2 == request.user else room.user2_id
        room_dict[friend_id] = room

    user_data = []

    for friend in friends:
        room = room_dict.get(friend.id)
        user_data.append({
            'user': friend,
            'latest_message': room.latest_message_content if room else '',
            'timestamp': room.latest_message_timestamp if room else None,
        })

    context = {
        'user_data': user_data,
        'query': query,
    }

    return render(request, 'myapp/friends.html', context)


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