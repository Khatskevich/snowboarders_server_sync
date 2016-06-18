from __future__ import unicode_literals

from django.contrib.gis.db import models

from rest.exceptions import MY_REST_EXCEPTION
from rest.http_statuses import HTTP_TRIP_STATUS_ERROR
from suser.models import User
from training.constants import TYPES_TRAINING, STATUSES_TRAINING


class Training(models.Model):
    status = models.IntegerField(choices=STATUSES_TRAINING, help_text=str(STATUSES_TRAINING))
    place_string = models.CharField(max_length=50)
    place_point = models.PointField(null=True, blank=True)
    type = models.IntegerField(choices=TYPES_TRAINING, help_text=str(TYPES_TRAINING))
    learner = models.ForeignKey(User, null=True, blank=True, related_name="trainings_as_learner")
    couch = models.ForeignKey(User, null=True, blank=True, related_name="trainings_as_couch")
    time_start = models.DateTimeField()
    @staticmethod
    def rest_update_single_column(queryset, parameters):
        updated_cnt = queryset.update(**parameters)
        if updated_cnt != 1:
            raise MY_REST_EXCEPTION(detail="You are late", status=HTTP_TRIP_STATUS_ERROR)
