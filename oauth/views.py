from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Client
from .serializers import ClientSerializer


@api_view(['POST'])
def token(request):
    client = ClientSerializer(data=request.data)
    if client.is_valid():
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user is not None:
            client = Client.objects.get(username=user.username)
            if client.token is None:
                client.generate_token()
                client.save()
            return Response({"token": client.token}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response({"error": client.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def invalidate_token(request):
    client = ClientSerializer(data=request.data)
    if client.is_valid():
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user is not None:
            client = Client.objects.get(username=user.username)
            client.invalidate_token()
            client.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response({"error": client.errors}, status=status.HTTP_400_BAD_REQUEST)
