from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from oauth.models import Client
from reviews.models import Company
from reviews.models import Reviewer

# get a list of companies
def companies(request):
    if request.method == 'GET':
        token = request.META['HTTP_X_AUTHORIZATION']
        if token:
            client = Client.objects.filter(token=token).first()
            if client is not None:
                companies = Company.objects.all()
                companies = [{"id": c.pk, "name": c.name, "rating": c.get_rating()} for c in companies]
                return JsonResponse({"companies": companies})
            return JsonResponse({"error": "A valid token is needed for this request."})
        return JsonResponse({"error": "A valid token is needed for this request."})
    return JsonResponse({'error': 'Http method not allowed'})

# get a list of reviewers
def reviewers(request):
    if request.method == 'GET':
        token = request.META['HTTP_X_AUTHORIZATION']
        if token:
            client = Client.objects.filter(token=token).first()
            if client is not None:
                reviewers = Reviewer.objects.all()
                reviewers = [{"id": r.pk, "name": r.name} for r in reviewers]
                return JsonResponse({"reviewers": reviewers})
            return JsonResponse({"error": "A valid token is needed for this request."})
        return JsonResponse({"error": "A valid token is needed for this request."})
    return JsonResponse({'error': 'Http method not allowed'})
