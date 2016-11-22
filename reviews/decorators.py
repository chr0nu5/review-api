from django.utils.functional import wraps
from rest_framework import status
from rest_framework.response import Response


def token_required():
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            token = request.META.get('HTTP_X_AUTHORIZATION', '')
            if len(token) == 36:
                return func(request, *args, **kwargs)
            return Response({"error": "This endpoint requires a token"}, status.HTTP_403_FORBIDDEN)
        return wraps(func)(inner_decorator)
    return decorator
