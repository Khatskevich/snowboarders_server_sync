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
        exclude = ('id','sender','creation_time',)

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
    chat = Chat.objects.filter(Q(dialogrelations__user_1=user) | Q(dialogrelations__user_2=user)).filter(id=sdata['chat'].pk).first()
    if chat is None:
        return Response("", status=HTTP_DOES_NOT_EXIST)
    message = Message()
    message.chat = chat
    message.sender = user
    message.text = sdata['text']
    message.save()


    TCP_IP = 'localhost'
    TCP_PORT = 43455
    MSG = MessageSerializer(message).data

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MSG)
    print MSG
    s.close()

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
        chat = Chat.objects.get(userchatrelations__user=user,id=sdata['id'])
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
    chats = Chat.objects.filter(Q(dialogrelations__user_1=user) | Q(dialogrelations__user_2=user))
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

def add_users_to_chat(chat, user_ids):
    for user_id in user_ids:
        try:
            chat_user = User.objects.get(id=user_id)
            user_chat_relation = UserChatRelation()
            user_chat_relation.chat = chat
            user_chat_relation.user = chat_user
            user_chat_relation.save()
        except Exception:
            return Response("", status=HTTP_DOES_NOT_EXIST)


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
    add_users_to_chat(chat, user_ids)
    return Response("", status=HTTP_OK)

@api_view(['POST'])
def get_chat_with_user(request):
    """
    Find or create chat with user
    ---
    response_serializer: ChatSerializer
    request_serializer: IdSerializer
    """
    sdata = get_validated_serializer(request=request, serializer=IdSerializer).validated_data
    user = get_user_from_validated_data(sdata)
    try:
        opponent = User.objects.get(id=sdata['id'])
    except Exception:
        return Response("", status=HTTP_DOES_NOT_EXIST)
    chat = DialogRelation.find_or_create(user,opponent)
    return Response(ChatSerializer(chat).data, status=HTTP_OK)


class GetChatHistorySerializer(IdSerializer):
    pass

@api_view(['POST'])
def get_chat_history(request):
    """
    ---
    response_serializer: MessageSerializer
    request_serializer: GetChatHistorySerializer
    """
    sdata = get_validated_serializer(request=request, serializer=GetChatHistorySerializer).validated_data
    user = get_user_from_validated_data(sdata)
    try:
        dialog_rel = DialogRelation.objects.get(id=sdata['id'])
        if dialog_rel.user_1 != user and dialog_rel.user_2 != user:
            raise Exception()
    except Exception:
        return Response("", status=HTTP_DOES_NOT_EXIST)
    messages = Message.objects.filter(chat=sdata['id']).order_by("-creation_time")
    return Response(MessageSerializer(messages, many=True).data, status=HTTP_OK)



