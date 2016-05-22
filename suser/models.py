# coding=utf-8
from __future__ import unicode_literals

import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.gis.db import models

# Create your models here.
from django.utils import timezone

from rest.exceptions import MY_REST_EXCEPTION
from rest.http_statuses import HTTP_DOES_NOT_EXIST
from suser.constants import PHONE_VALIDATORS


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'img/users/' + filename


class UserManager(BaseUserManager):
    def _create_user(self, phone, email, password, first_name, last_name, is_staff,
                     is_superuser, **extra_fields):
        now = timezone.now()
        if not phone:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, first_name=first_name, last_name=last_name,
                          is_staff=is_staff, is_active=False,
                          is_superuser=is_superuser, last_login=now,
                          registration_time=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, password=None, first_name=None, last_name=None,
                    **extra_fields):
        return self._create_user(phone, email, password, first_name, last_name, False, False,
                                 **extra_fields)

    def create_superuser(self, phone, email, password, first_name, last_name,
                         **extra_fields):
        user = self._create_user(phone, email, password, first_name, last_name, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    image = models.ImageField(upload_to=get_file_path,
                              default='img/users/default.png',
                              null=True,
                              blank=True)
    phone = models.CharField(max_length=30, unique=True,
                             help_text=('Phone number 9123456789'),
                             validators=PHONE_VALIDATORS)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False,
                                   help_text=('Designates whether the user can log into this admin '
                                              'site.'))
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    registration_time = models.DateTimeField(auto_now_add=True)
    last_point = models.PointField(blank=True, null=True, help_text="last lang and lat")
    position_measurement_time = models.DateTimeField(blank=True, null=True)
    rating = models.FloatField(default=0)
    is_couch = models.BooleanField(default=False)
    google_cloud_id = models.CharField(max_length=200,
                                       help_text="Id which user (dr and cus) takes from google cloud, for downstream messagging.",
                                       null=True, blank=True)
    short_info = models.TextField(help_text="Short info about user",
                                       null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    @staticmethod
    def rest_get(pk):
        try:
            return User.objects.get(pk=pk)
        except Exception:
            raise MY_REST_EXCEPTION(detail="Wring user id", status=HTTP_DOES_NOT_EXIST)

    def has_image(self):
        # We should add check image existence
        if self.image.name == "default.png":
            return False
        return True

    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'