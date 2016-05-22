from rest_framework.exceptions import APIException

class MY_REST_EXCEPTION(APIException):
    def __init__(self, status, detail=""):
        self.status_code = status
        self.detail = detail