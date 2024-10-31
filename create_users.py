import os
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings.dev")
django.setup()

from accounts.models import CustomUser
from myapp.models import Message, ChatRoom

fakegen = Faker(["ja_JP"])

def create_users(n):

    users = [
        CustomUser(username=fakegen.user_name(), email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]
    CustomUser.objects.bulk_create(users, ignore_conflicts=True)

    my_id = CustomUser.objects.get(username="admin").id

    user_ids = CustomUser.objects.exclude(id=my_id).values_list("id", flat=True)

    chatrooms = []
    for user_id in user_ids:
        chatroom = ChatRoom(user1_id=my_id, user2_id=user_id)
        chatrooms.append(chatroom)
    ChatRoom.objects.bulk_create(chatrooms,ignore_conflicts=True)


    talks = []
    for chatroom in ChatRoom.objects.all():
        sent_talk = Message(
            sender_id=my_id,
            content=fakegen.text(),
            room = chatroom
        )
        received_talk = Message(
            sender_id=random.choice(user_ids),
            content=fakegen.text(),
            room=chatroom
        )
        talks.extend([sent_talk, received_talk])
    Message.objects.bulk_create(talks, ignore_conflicts=True)

    talks = Message.objects.order_by("-timestamp")[: 2 * len(user_ids)]
    for talk in talks:
        talk.time = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    Message.objects.bulk_update(talks, fields=["timestamp"])


if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(955)
    print("done")