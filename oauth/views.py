import uuid

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Client

@csrf_exempt
def token(request):
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username and password:
            user = authenticate(username = username, password = password)
            if user is not None:
                user = Client.objects.get(username=user.username)
                token = uuid.uuid4()
                user.token = token
                user.save()
                return JsonResponse({'token': user.token})
            return JsonResponse({'error': 'Invalid username or password'})
        return JsonResponse({'error': 'Username and password required'})
    return JsonResponse({'error': 'Http method not allowed'})
