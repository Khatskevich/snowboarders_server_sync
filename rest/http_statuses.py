HTTP_OK = 200

HTTP_ERROR = 400
HTTP_DOES_NOT_EXIST = 404  # for example - getting user by id which is not exists
HTTP_WRONG_SESSION = 401  # SESSION
HTTP_YOUR_TYPE_OF_USER_CANNOT_DO_THIS = 405
HTTP_LATE = 409  # For example : when you trying to take order which is already taken
HTTP_IT_IS_NOT_YOUR_OBJECT = 468
HTTP_WRONG_REQUEST_FORMAT = 470  # wrong format of data in request ( required field is messing or something...)
HTTP_IT_IS_CURRENTLY_PERFORMED = 208
HTTP_TRIP_STATUS_ERROR = 467