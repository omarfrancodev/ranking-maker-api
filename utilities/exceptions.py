from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import datetime

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    exception_type = type(exc).__name__
    exception_value = str(exc)
    request_method = context['request'].method
    request_url = context['request'].get_full_path()
    server_time = str(datetime.datetime.now())

    if response is not None:
        view = context.get('view', None)
        message = "There was an error processing the request."
        if view:
            message = f"Error processing {request_method} request for {view.get_view_name()}."
        
        custom_response = {
            'status': response.status_code,
            'data': {
                "error": "An error has occurred",
                "exception_type": exception_type,
                "request_method": request_method,
                "request_url": request_url,
                "server_time": server_time,
                "details": response.data
            },
            'message': message
        }
        return Response(custom_response, status=response.status_code)

    return Response({
        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'data': {
            "error": "An internal server error occurred.",
            "exception_type": exception_type,
            "request_method": request_method,
            "request_url": request_url,
            "server_time": server_time,
            "details": exception_value,
        },
        'message': 'An internal server error occurred.'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)