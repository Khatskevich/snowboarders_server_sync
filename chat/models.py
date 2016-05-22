# coding=utf-8
from django.db import models
from suser.models import User


class Chat(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    creation_time = models.DateTimeField(auto_now_add=True, editable=True)

class UserChatRelation(models.Model):
    chat_id = models.ForeignKey(Chat, db_index=True,related_name='userchatrelations')
    user_id = models.ForeignKey(User, db_index=True,related_name='userchatrelations')

class Message(models.Model):
    sender_id = models.ForeignKey(User, db_index=True)
    chat_id = models.ForeignKey(Chat, db_index=True)
    creation_time = models.DateTimeField(auto_now_add=True, editable=True)
    text = models.TextField()
