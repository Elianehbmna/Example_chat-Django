from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


class Convo(models.Model):
    uuid = models.CharField(max_length=100)
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.uuid


class Message(models.Model):
    convo = models.ForeignKey(Convo, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.content

