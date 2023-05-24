from django.db import models
from django.contrib.auth.models import User

import random
import string

from resources.models import FarmerGroup


def generate_uuid(length=6):
    """
    Generate a random UUID consisting of {length} letters and numbers.
    """
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    uuid = ''.join(random.choice(characters) for _ in range(length))
    return uuid


# Create your models here.

class UserChatGroup(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, null=False, related_name="user_1")
    user_2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, null=False, related_name="user_2")
    chat_name = models.CharField(blank=True, null=True, max_length=20)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.chat_name

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a new UUID for a new instance of the model
            while True:
                chat_name = generate_uuid(10)
                if not UserChatGroup.objects.filter(chat_name=chat_name).exists():
                    self.chat_name = chat_name
                    break

        return super().save(*args, **kwargs)


class ChatFile(models.Model):
    file = models.FileField(upload_to="user-chats/files/", blank=False, null=False)
    file_type = models.CharField(max_length=5, blank=True, null=True)


class ChatMessage(models.Model):
    chat_group = models.ForeignKey(UserChatGroup, blank=False, null=True, on_delete=models.SET_NULL)
    sender = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL)
    text = models.TextField(blank=False, null=False)
    files = models.ManyToManyField(ChatFile, blank=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)


class GroupChatMessage(models.Model):
    group = models.ForeignKey(FarmerGroup, blank=False, null=True, on_delete=models.SET_NULL)
    sender = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL)
    text = models.TextField(blank=False, null=False)
    files = models.ManyToManyField(ChatFile, blank=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)


