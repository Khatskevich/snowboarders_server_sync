import logging

from rest_framework.exceptions import APIException

logr_requests = logging.getLogger('requests')

class MY_REST_EXCEPTION(APIException):
    def __init__(self, status, detail=""):
        self.status_code = status
        self.detail = detail
        logr_requests.info(str(status) + " " + str(detail))