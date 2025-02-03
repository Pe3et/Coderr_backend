from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Changes 401 status codes to 403
    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        response.status_code = status.HTTP_403_FORBIDDEN

    # Custom error text for 403
    if response is not None and response.status_code == status.HTTP_403_FORBIDDEN:
        response.data['detail'] = 'Berechtigungsfehler.'

    return response