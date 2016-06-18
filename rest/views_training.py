import socket

from django.db.models import Q
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from chat.models import Chat, Message, UserChatRelation, DialogRelation
from rest.http_statuses import HTTP_DOES_NOT_EXIST, HTTP_OK
from rest.rest_helper import get_validated_serializer, get_user_from_validated_data
from rest.serializers import IdSerializer, UserSerializer, UserHashSerializer
from suser.models import User
from training.models import Training


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        exclude = ()



@api_view(['POST'])
def get_my_list(request):
    """
    ---
    request_serializer: UserHashSerializer
    response_serializer: TrainingSerializer
    """
    sdata = get_validated_serializer(request=request, serializer=UserHashSerializer).validated_data
    user = get_user_from_validated_data(sdata)
    trainings = Training.objects.filter(couch=user)
    return Response(TrainingSerializer(trainings, many=True).data, status=HTTP_OK)


@api_view(['POST'])
def get_my(request):
    """
    ---
    response_serializer: TrainingSerializer
    request_serializer: IdSerializer
    responseMessages:
        - code: HTTP_DOES_NOT_EXIST
          message: doesn't exist
    """
    sdata = get_validated_serializer(request=request, serializer=IdSerializer).validated_data
    user = get_user_from_validated_data(sdata)
    try:
        training = Training.objects.get(id=sdata['id'])
        if training.couch != user and training.learner != user:
            raise Exception()
    except Exception:
        return Response("", status=HTTP_DOES_NOT_EXIST)

    return Response(TrainingSerializer(training).data, status=HTTP_OK)

@api_view(['POST'])
def create(request):
    """
    ---
    request_serializer: TrainingSerializer
    """
    sdata = get_validated_serializer(request=request, serializer=IdSerializer).validated_data
    user = get_user_from_validated_data(sdata)
    training = Training(learner=user,**sdata)
    training.save()
    return Response("", status=HTTP_OK)
