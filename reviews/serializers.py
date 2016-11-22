from rest_framework import serializers
from .models import Company
from .models import Reviewer
from .models import Review
from oauth.models import Client


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name',)


class ReviewerSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='username', queryset=Client.objects.all())

    class Meta:
        model = Reviewer
        fields = ('id', 'name', 'email', 'client')


class ReviewSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field='id', queryset=Company.objects.all())
    reviewer = serializers.SlugRelatedField(slug_field='id', queryset=Reviewer.objects.all())
    client = serializers.SlugRelatedField(slug_field='username', queryset=Client.objects.all())

    class Meta:
        model = Review
        fields = ('id', 'rating', 'title', 'summary', 'ip', 'company', 'reviewer', 'client')
