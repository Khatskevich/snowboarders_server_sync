from django.db.models import Q
from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest.http_statuses import HTTP_DOES_NOT_EXIST, HTTP_OK
from rest.rest_helper import get_validated_serializer, get_user_from_validated_data
from rest.serializers import IdSerializer, UserHashSerializer
from training.constants import STATUSES_TRAINING, S_WAITS_FOR_COUCH
from training.models import Training


class TrainingSerializer(serializers.ModelSerializer):
    place_point = PointField(required=False)
    class Meta:
        model = Training
        exclude = ()


class TrainingCreateSerializer(UserHashSerializer, serializers.ModelSerializer):
    place_point = PointField(required=False)
    class Meta:
        model = Training
        exclude = ('learner','status',)

class GetMyListSerializer(UserHashSerializer):
    statuses = serializers.ListField(
        child=serializers.ChoiceField(choices=STATUSES_TRAINING)
    )
    i_am_as = serializers.ChoiceField(choices=(('l','learner'), ('c','couch'),))

class GetListSerializer(UserHashSerializer):
    pass

@api_view(['POST'])
def get_my_list(request):
    """
    ---
    request_serializer: GetMyListSerializer
    response_serializer: TrainingSerializer
    """
    sdata = get_validated_serializer(request=request, serializer=GetMyListSerializer).validated_data
    user = get_user_from_validated_data(sdata)
    if sdata["i_am_as"] == 'l':
        trainings = Training.objects.filter(learner=user)
    else:
        trainings = Training.objects.filter(couch=user)
    if 'statuses' in sdata and len(sdata['statuses']) > 0:
        status_query = None
        for s in sdata['statuses']:
            if status_query==None:
                status_query = Q(status=s)
            else:
                status_query= status_query | Q(status=s)
        trainings = trainings.filter(status_query)
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
    parameters:
        -
            name: place_point
            type: string
    request_serializer: TrainingCreateSerializer
    """
    sdata = get_validated_serializer(request=request, serializer=TrainingCreateSerializer).validated_data
    user = get_user_from_validated_data(sdata)
    training = Training(learner=user,status=S_WAITS_FOR_COUCH, **sdata)
    training.save()
    return Response("", status=HTTP_OK)

@api_view(['POST'])
def get_list(request):
    """
    ---
    request_serializer: GetListSerializer
    response_serializer: TrainingSerializer
    responseMessages:
        - code: HTTP_YOUR_TYPE_OF_USER_CANNOT_DO_THIS
          message: user is not a couch
    """
    sdata = get_validated_serializer(request=request, serializer=GetListSerializer).validated_data
    user = get_user_from_validated_data(sdata, check_couch=True)
    trainings = Training.objects.filter(status=S_WAITS_FOR_COUCH)
    return Response(TrainingSerializer(trainings, many=True).data, status=HTTP_OK)