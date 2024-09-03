from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class WrongCredentialsGivenException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Wrong email or password given"


class TokenAbsentException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token absent"


class IncorrectTokenFormatException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class TokenExpiredException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class UserIsNotPresentException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED


class NotFoundException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"


class AddException(Exception):
    pass
