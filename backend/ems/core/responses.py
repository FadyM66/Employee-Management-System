from rest_framework.response import Response
from rest_framework import status

class ClassProperty:
    """Descriptor for class properties"""
    def __init__(self, fget):
        self.fget = fget
        
    def __get__(self, instance, owner):
        return self.fget(owner)

class Responses:
    """
    Centralized API response handler for consistent error/success messaging
    
    Usage:
        Responses.missing_data  # Returns 400 with standard message
        Responses.invalid_data  # Returns 400 with validation errors
        to add data or details:
        Responses.set_data(data).invalid_data
        
    """
    _data = None
    
    @classmethod
    def set_data(cls, data):
        cls._data = data
        return cls
    
    # Client Errors (4xx)
    @ClassProperty
    def missing_data(cls):
        """400 - Request missing required data"""
        data = cls._data
        
        return Response(
            {"error": "No data provided", **({"data": data} if data else {})},
            status=status.HTTP_400_BAD_REQUEST
        )

    @ClassProperty
    def invalid_data(cls):
        """400 - Invalid request data format"""
        data = cls._data
        return Response(
            {"error": "Invalid data provided", **({"data": data} if data else {})},
            status=status.HTTP_400_BAD_REQUEST
        )

    @ClassProperty
    def unauthorized(cls):
        """401 - Authentication required"""
        data = cls._data
        return Response(
            {"error": "Authentication required", **({"data": data} if data else {})},
            status=status.HTTP_401_UNAUTHORIZED
        )

    @ClassProperty
    def forbidden(cls):
        """403 - Insufficient permissions"""
        data = cls._data
        return Response(
            {"error": "You don't have permission for this action", **({"data": data} if data else {})},
            status=status.HTTP_403_FORBIDDEN
        )

    @ClassProperty
    def not_found(cls):
        """404 - Resource not found"""
        data = cls._data
        return Response(
            {"error": "Requested resource not found", **({"data": data} if data else {})},
            status=status.HTTP_404_NOT_FOUND
        )

    @ClassProperty
    def method_not_allowed(cls):
        """405 - Invalid HTTP method"""
        data = cls._data
        return Response(
            {"error": "HTTP method not allowed", **({"data": data} if data else {})},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @ClassProperty
    def conflict(cls):
        """409 - Resource conflict"""
        data = cls._data
        return Response(
            {"error": "Resource already exists", **({"data": data} if data else {})},
            status=status.HTTP_409_CONFLICT
        )

    # Server Errors (5xx)
    @ClassProperty
    def server_error(cls):
        """500 - Generic server error"""
        data = cls._data
        return Response(
            {"error": "Internal server error", **({"data": data} if data else {})},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Success Responses (2xx)
    @ClassProperty
    def created(cls):
        """201 - Resource created successfully"""
        data = cls._data
        return Response(
            {"message": "Resource created successfully", **({"data": data} if data else {})},
            status=status.HTTP_201_CREATED
        )

    @ClassProperty
    def ok(cls):
        data = cls._data
        return Response(
            {"message": "Operation completed successfully", **({"data": data} if data else {})},
            status=status.HTTP_200_OK
        )