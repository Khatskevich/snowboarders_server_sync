import logging

from rest.exceptions import MY_REST_EXCEPTION
from rest.http_statuses import HTTP_WRONG_REQUEST_FORMAT, HTTP_WRONG_SESSION, HTTP_YOUR_TYPE_OF_USER_CANNOT_DO_THIS
from session.models import Session

logr_requests = logging.getLogger('requests')

def get_user_from_validated_data(data):
    user = None
    try:
        hash = data['hash']
        session = Session.getSession(hash)
        del data['hash']
        user = session.user
    except Exception:
        raise MY_REST_EXCEPTION(detail="Wrong session", status=HTTP_WRONG_SESSION)
    return user

def get_validated_serializer(request, serializer):
    logr_requests.info(request.path + " " + str(request.data))
    serializer_object = serializer(data=request.data)
    if not serializer_object.is_valid():
        raise MY_REST_EXCEPTION(detail=serializer_object.errors, status=HTTP_WRONG_REQUEST_FORMAT)
    return serializer_object