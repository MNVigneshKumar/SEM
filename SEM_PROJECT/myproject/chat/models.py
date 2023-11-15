from django.db import models
from datetime import datetime
from pedal.models import AppUser
from django.contrib.auth.models import User


# Create your models here.
class Room(models.Model):
    name = models.TextField(max_length=2500)
    cycle_id = models.TextField(max_length=1000)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)


class Message(models.Model):
    value = models.TextField(max_length=2500)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.TextField(max_length=2500)
    room = models.TextField(max_length=2500)
