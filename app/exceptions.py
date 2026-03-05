from typing import Optional
from fastapi import HTTPException, status

class BaseAPIException(HTTPException):
    """Base exception for API errors"""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: Optional[list] = None
    ):
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.data = data or []

class UnauthorizedException(BaseAPIException):
    """Unauthorized access exception"""
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class ForbiddenException(BaseAPIException):
    """Forbidden access exception"""
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )

class NotFoundException(BaseAPIException):
    """Resource not found exception"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )

class ConflictException(BaseAPIException):
    """Resource conflict exception"""
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT
        )

class ValidationException(BaseAPIException):
    """Validation error exception"""
    def __init__(self, message: str = "Validation failed", data: Optional[list] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            data=data
        )

class DatabaseException(BaseAPIException):
    """Database operation exception"""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )