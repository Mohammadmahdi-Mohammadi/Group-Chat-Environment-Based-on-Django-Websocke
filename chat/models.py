from datetime import datetime
import random

from django.db import models
from django.contrib.auth.models import User


def UniqueGenerator(length=10):
    source = "abcdefghijklmnopqrztuvwxyz"
    result = ""
    for _ in range(length):
        result += source[random.randint(0, length)]
    return result


class GroupChat(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    unique_code = models.CharField(max_length=10, default=UniqueGenerator)
    date_created = models.DateTimeField(default=datetime.now)


class Member(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default="")
    date_created = models.DateTimeField(default=datetime.now)

class Forbidden(models.Model):
    Forbiden_msg = models.CharField(max_length=15,primary_key=True)
    active_flag = models.BooleanField(default=False, null=True)

