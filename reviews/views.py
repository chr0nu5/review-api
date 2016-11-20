import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from oauth.models import Client
from reviews.models import Company
from reviews.models import Reviewer
from reviews.models import Review
from django.views.decorators.csrf import csrf_exempt

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
@csrf_exempt
def reviewers(request):
    token = request.META['HTTP_X_AUTHORIZATION']
    if token:
        client = Client.objects.filter(token=token).first()
        if client is not None:
            if request.method == 'GET':
                reviewers = Reviewer.objects.filter(client=client)
                reviewers = [{"id": r.pk, "name": r.name} for r in reviewers]
                return JsonResponse({"reviewers": reviewers})
            elif request.method == 'POST':
                name = request.POST.get('name','')
                email = request.POST.get('email','')
                if name and email:
                    match = re.search(r'[\w.-]+@[\w.-]+.\w+', email)
                    if match:
                        reviewer = Reviewer.objects.create(name=name, email=email, client=client)
                        reviewer = {
                            "id": reviewer.pk,
                            "name": reviewer.name,
                            "email": reviewer.email,
                        }
                        return JsonResponse({'reviewer': reviewer})
                    else:
                        return JsonResponse({'error': 'You must provide a valid email'})
                return JsonResponse({'error': 'You must provide a name and an email'})
            else:
                return JsonResponse({'error': 'Http method not allowed'})
        return JsonResponse({"error": "A valid token is needed for this request."})
    return JsonResponse({"error": "A valid token is needed for this request."})

def reviews(request):
    token = request.META['HTTP_X_AUTHORIZATION']
    if token:
        client = Client.objects.filter(token=token).first()
        if client is not None:
            if request.method == 'GET':
                reviews = Review.objects.filter(client=client)
                reviews = [{
                    "id": r.pk,
                    "rating": r.rating,
                    "title": r.title,
                    "summary": r.summary,
                    "ip": r.ip,
                    "company": {
                        "id": r.company.pk,
                        "name": r.company.name
                    },
                    "reviewer": {
                        "id": r.reviewer.pk,
                        "name": r.reviewer.name,
                        "email": r.reviewer.email
                    },
                    "date": r.created_date
                } for r in reviews]
                return JsonResponse({'reviews': reviews})
            elif request.method == 'POST':
                pass
            else:
                return JsonResponse({'error': 'Http method not allowed'})
        return JsonResponse({"error": "A valid token is needed for this request."})
    return JsonResponse({"error": "A valid token is needed for this request."})
