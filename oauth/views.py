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
                client = Client.objects.get(username=user.username)
                client.generate_token()
                client.save()
                return JsonResponse({'token': client.get_token()})
            return JsonResponse({'error': 'Invalid username or password'})
        return JsonResponse({'error': 'Username and password required'})
    return JsonResponse({'error': 'Http method not allowed'})

@csrf_exempt
def invalidate_token(request):
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username and password:
            user = authenticate(username = username, password = password)
            if user is not None:
                client = Client.objects.get(username=user.username)
                client.invalidate_token()
                client.save()
                return JsonResponse({'msg': 'User token has been invalidated'})
            return JsonResponse({'error': 'Invalid username or password'})
        return JsonResponse({'error': 'Username and password required'})
    return JsonResponse({'error': 'Http method not allowed'})
