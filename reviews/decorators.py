from django.utils.functional import wraps
from rest_framework import status
from rest_framework.response import Response
from oauth.models import Client


def token_required():
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            token = request.META.get('HTTP_X_AUTHORIZATION', '')
            if len(token) != 36:
                return Response({"error": "Invalid token"}, status.HTTP_403_FORBIDDEN)
            client = Client.objects.filter(token=token).first()
            if client is None:
                return Response({"error": "Client does not exists"}, status=status.HTTP_401_UNAUTHORIZED)
            request.client = client
            return func(request, *args, **kwargs)
        return wraps(func)(inner_decorator)
    return decorator
