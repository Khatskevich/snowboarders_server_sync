# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
import hashlib
from suser.models import User
from datetime import datetime


class Session(models.Model):
    hash = models.CharField(max_length=64, unique=True,
                            help_text=('Unic hash of the session'), blank=False, null=False)
    user = models.ForeignKey(User, null=False, blank=False, related_name='sessions')
    creation_time = models.DateTimeField(auto_now=True, editable=True)

    def __unicode__(self):
        return 'Session # ' + str(self.pk)

    @staticmethod
    def getSession(hash):
        try:
            session = Session.objects.get(hash=hash)
            return session
        except:
            raise serializers.ValidationError("Wrong session!!!")
    @staticmethod
    def get_for_user(user):
        sessions = user.sessions.all()
        if sessions.count() > 0:
            return sessions[0]
        session = Session()
        session.hash = hashlib.sha256(str(user.pk) + str(datetime.now())).hexdigest()
        session.user = user
        session.save()
        return session

    class Meta:
        verbose_name = u'Сессия'
        verbose_name_plural = u'Сессии'