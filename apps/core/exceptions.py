"""
Custom exception handlers for tu_credito project.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc: Exception, context: dict) -> Response:
    """
    Custom exception handler that provides consistent error responses.
    
    Args:
        exc: The exception that was raised
        context: Dictionary containing context information about the exception
        
    Returns:
        Response: DRF Response object with standardized error format
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the response data
        custom_response_data = {
            'error': True,
            'message': 'Ha ocurrido un error',
            'details': response.data,
            'status_code': response.status_code,
        }
        
        # Log the error
        logger.error(
            f"Error: {exc}",
            extra={
                'exception': str(exc),
                'context': context,
                'status_code': response.status_code,
            }
        )
        
        response.data = custom_response_data
    
    else:
        # Handle unexpected exceptions
        logger.exception(
            "Unexpected error occurred",
            extra={
                'exception': exc,
                'context': context,
            }
        )
        
        response = Response(
            {
                'error': True,
                'message': 'Ha ocurrido un error inesperado',
                'details': {'non_field_errors': [str(exc)]},
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response
