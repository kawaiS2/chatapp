from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='media_local', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username
