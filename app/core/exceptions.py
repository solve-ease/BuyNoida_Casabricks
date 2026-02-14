"""
Custom exceptions for the application
"""


class BaseAPIException(Exception):
    """Base exception for API errors"""
    def __init__(self, message: str = "An error occurred", status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class PropertyNotFoundException(BaseAPIException):
    """Exception raised when a property is not found"""
    def __init__(self, property_id: str):
        super().__init__(
            message=f"Property with ID {property_id} not found",
            status_code=404
        )


class InquiryNotFoundException(BaseAPIException):
    """Exception raised when an inquiry is not found"""
    def __init__(self, inquiry_id: str):
        super().__init__(
            message=f"Inquiry with ID {inquiry_id} not found",
            status_code=404
        )


class ImageNotFoundException(BaseAPIException):
    """Exception raised when an image is not found"""
    def __init__(self, image_id: str):
        super().__init__(
            message=f"Image with ID {image_id} not found",
            status_code=404
        )


class UserNotFoundException(BaseAPIException):
    """Exception raised when a user is not found"""
    def __init__(self, identifier: str):
        super().__init__(
            message=f"User {identifier} not found",
            status_code=404
        )


class UnauthorizedException(BaseAPIException):
    """Exception raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message, status_code=401)


class ForbiddenException(BaseAPIException):
    """Exception raised when user doesn't have permission"""
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message=message, status_code=403)


class ValidationException(BaseAPIException):
    """Exception raised when validation fails"""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=400)


class RateLimitException(BaseAPIException):
    """Exception raised when rate limit is exceeded"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message=message, status_code=429)


class ImageEnhancementException(BaseAPIException):
    """Exception raised when image enhancement fails"""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=500)


class StorageException(BaseAPIException):
    """Exception raised when storage operations fail"""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=500)
