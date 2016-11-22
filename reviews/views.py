from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Company
from .models import Reviewer
from .models import Review
from .utils import get_ip

from .decorators import token_required
from .serializers import CompanySerializer
from .serializers import ReviewerSerializer
from .serializers import ReviewSerializer


@api_view(['GET'])
@token_required()
def companies(request):
    serializer = CompanySerializer(Company.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@token_required()
def reviewers(request):
    if request.method == 'GET':
        serializer = ReviewerSerializer(Reviewer.objects.filter(client=request.client), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = {
            "name": request.data.get('name'),
            "email": request.data.get('email'),
            "client": request.client.username,
        }
        serializer = ReviewerSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@token_required()
def reviews(request):
    if request.method == 'GET':
        serializer = ReviewSerializer(Review.objects.filter(client=request.client), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = {
            "rating": request.data.get('rating'),
            "title": request.data.get('title'),
            "summary": request.data.get('summary'),
            "ip": get_ip(request),
            "company": request.data.get('company_id'),
            "reviewer": request.data.get('reviewer_id'),
            "client": request.client.username
        }
        serializer = ReviewSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
