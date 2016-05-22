from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from chat.models import Chat, Message, UserChatRelation
from rest.http_statuses import HTTP_DOES_NOT_EXIST, HTTP_OK
from rest.rest_helper import get_validated_serializer, get_user_from_validated_data
from rest.serializers import IdSerializer, UserSerializer, UserHashSerializer
from suser.models import User


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        exclude = ()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ()

class MessageSendSerializer(serializers.ModelSerializer, UserHashSerializer):
    class Meta:
        model = Message
        exclude = ('id','sender_id','creation_time',)

@api_view(['POST'])
def send_message(request):
    """
    ---
    request_serializer: MessageSendSerializer
    responseMessages:
        - code: HTTP_DOES_NOT_EXIST
          message: doesn't exist
    """
    sdata = get_validated_serializer(request=request, serializer=MessageSendSerializer).validated_data
    user = get_user_from_validated_data(sdata)
    try:
        UserChatRelation.objects.get(chat_id=sdata['chat_id'],user_id=sdata['user_id'])
        chat = Chat.objects.get(id=sdata['chat_id'])
    except Exception:
        return Response("", status=HTTP_DOES_NOT_EXIST)
    message = Message()
    message.chat_id = chat
    message.sender_id = user
    message.text = sdata['text']
    message.save()
    return Response("", status=HTTP_OK)


@api_view(['POST'])
def get_my(request):
    """
    ---
    response_serializer: ChatSerializer
    request_serializer: IdSerializer
    responseMessages:
        - code: HTTP_DOES_NOT_EXIST
          message: doesn't exist
    """
    sdata = get_validated_serializer(request=request, serializer=IdSerializer).validated_data
    user = get_user_from_validated_data(sdata)
    try:
        chat = Chat.objects.get(userchatrelations__user_id=user,id=sdata['id'])
    except Exception:
        return Response("", status=HTTP_DOES_NOT_EXIST)
    return Response(ChatSerializer(chat).data, status=HTTP_OK)

@api_view(['POST'])
def get_my_list(request):
    """
    ---
    response_serializer: ChatSerializer
    request_serializer: UserHashSerializer
    """
    sdata = get_validated_serializer(request=request, serializer=UserHashSerializer).validated_data
    user = get_user_from_validated_data(sdata)
    chats = Chat.objects.filter(userchatrelations__user_id=user)
    return Response(ChatSerializer(chats,many=True).data, status=HTTP_OK)

class CreateChatSerializer(serializers.ModelSerializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(required=False),
        required=True,
        help_text=('')
    )
    class Meta:
        model = Chat
        exclude = ('id','creation_time',)

@api_view(['POST'])
def create(request):
    """
    ---
    request_serializer: CreateChatSerializer
    """
    sdata = get_validated_serializer(request=request, serializer=CreateChatSerializer).validated_data
    user = get_user_from_validated_data(sdata)
    chat = Chat()
    chat.name = sdata['name']
    chat.save()
    user_ids = sdata['user_ids']
    if user.pk not in user_ids:
        user_ids.append(user.pk)
    for user_id in user_ids:
        try:
            chat_user = User.objects.get(id=user_id)
            user_chat_relation = UserChatRelation()
            user_chat_relation.chat_id = chat
            user_chat_relation.user_id = chat_user
            user_chat_relation.save()
        except Exception:
            return Response("", status=HTTP_DOES_NOT_EXIST)
    return Response("", status=HTTP_OK)
