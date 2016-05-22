# coding=utf-8
from django.db import models

from chat.constants import CHAT_TYPES, DIALOG
from suser.models import User


class Chat(models.Model):
    type = models.IntegerField(choices=CHAT_TYPES, default=DIALOG, null=False, blank=False, help_text=str(CHAT_TYPES))
    name = models.CharField(max_length=20, blank=False, null=False)
    creation_time = models.DateTimeField(auto_now_add=True, editable=True)

class UserChatRelation(models.Model):
    chat_id = models.ForeignKey(Chat, db_index=True,related_name='userchatrelations')
    user_id = models.ForeignKey(User, db_index=True,related_name='userchatrelations')

class DialogRelation(models.Model):
    chat_id = models.ForeignKey(Chat, db_index=True,related_name='dialogrelations')
    user_1 = models.ForeignKey(User, db_index=True,related_name='user_1_chat')
    user_2 = models.ForeignKey(User, db_index=True,related_name='user_2_chat')

    @staticmethod
    def find_or_create(user_1, user_2):
        if user_1.pk > user_2.pk:
            user = user_1
            user_1 = user_2
            user_2 = user
        dialog = DialogRelation.objects.filter(user_1=user_1, user_2 = user_2).first()
        if dialog != None:
            return dialog.chat_id
        chat = Chat()
        chat.name = user_1.first_name + " " + user_2.first_name
        chat.save()
        dialog = DialogRelation()
        dialog.chat_id = chat
        dialog.user_1 = user_1
        dialog.user_2 = user_2
        dialog.save()
        return chat

class Message(models.Model):
    sender_id = models.ForeignKey(User, db_index=True)
    chat_id = models.ForeignKey(Chat, db_index=True)
    creation_time = models.DateTimeField(auto_now_add=True, editable=True)
    text = models.TextField()
