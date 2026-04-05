from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response({
            "status": "error",
            "message": "Something went wrong",
            "details": response.data
        }, status=response.status_code)

    return Response({
        "status": "error",
        "message": "Server error"
    }, status=500)