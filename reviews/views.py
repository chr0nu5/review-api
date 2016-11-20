import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from oauth.models import Client
from reviews.models import Company
from reviews.models import Reviewer
from reviews.models import Review
from django.views.decorators.csrf import csrf_exempt
from utils import get_ip

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

# get a list of reviewers or add a new reviewer
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

# get a list of reviews or add a new review
@csrf_exempt
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
                rating = request.POST.get('rating', '')
                title = request.POST.get('title', '')
                summary = request.POST.get('summary', '')
                ip = get_ip(request)
                company = request.POST.get('company_id', '')
                #company = Company.objects.filter(pk=company).first()
                reviewer = request.POST.get('reviewer_id', '')
                #reviewer = Reviewer.objects.filter(pk=reviewer).first()

                try:
                    rating = int(rating)
                    if rating < 0 or rating > 5:
                        return JsonResponse({'error': 'Rating must be a integer number between 0 and 5'})
                except ValueError:
                    return JsonResponse({'error': 'Rating must be a integer number'})

                if not title:
                    return JsonResponse({'error': 'You must provide a title'})

                if len(summary) == 0 or len(summary) > 10000:
                    return JsonResponse({'error': 'You must provide a `summary` and it cannot have more than 10.000 characters'})

                if not ip:
                    return JsonResponse({'error': 'You must be hiding from me'})

                if not company:
                    return JsonResponse({'error': 'You must provide a `company_id`'})
                else:
                    company = Company.objects.filter(pk=company).first()
                    if company is None:
                        return JsonResponse({'error': 'Provided `company_id` does not exists'})

                if not reviewer:
                    return JsonResponse({'error': 'You must provide a `reviewer_id`'})
                else:
                    reviewer = Reviewer.objects.filter(pk=reviewer).first()
                    if reviewer is None:
                        return JsonResponse({'error': 'Provided `reviewer_id` does not exists'})

                review = Review(rating=rating, title=title, summary=summary, ip=ip, company=company, reviewer=reviewer, client=client)
                try:
                    review.clean_fields()
                    review.save()
                except Exception, error:
                    print str(error)
                    return JsonResponse({"error": str(error)})

                return JsonResponse({"review": {
                        "id": review.pk,
                        "rating": review.rating,
                        "title": review.title,
                        "summary": review.summary,
                        "ip": review.ip,
                        "company": {
                            "id": review.company.pk,
                            "name": review.company.name
                        },
                        "reviewer": {
                            "id": review.reviewer.pk,
                            "name": review.reviewer.name,
                            "email": review.reviewer.email
                        },
                        "date": review.created_date
                    }})
            else:
                return JsonResponse({'error': 'Http method not allowed'})
        return JsonResponse({"error": "A valid token is needed for this request."})
    return JsonResponse({"error": "A valid token is needed for this request."})
