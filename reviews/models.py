from __future__ import unicode_literals

from django.db import models
from django.db.models import Avg
from django.core.exceptions import ValidationError
from oauth.models import Client

def validate_rating(value):
    try:
        value = int(value)
        if value < 0 or value > 5:
            raise ValidationError('Invalid rating')
    except ValueError:
        raise ValidationError('Invalid rating')

def validate_summary(value):
    print len(value)
    if len(value) > 10000:
        raise ValidationError('Invalid summary')

class Company(models.Model):
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['-pk']

    def get_rating(self):
        return Review.objects.filter(company=self).aggregate(Avg('rating'))['rating__avg']

class Reviewer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    client = models.ForeignKey(Client)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Reviewer"
        verbose_name_plural = "Reviewers"
        ordering = ['-pk']

class Review(models.Model):
    rating = models.IntegerField(validators=[validate_rating])
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=10000, validators=[validate_summary])
    ip = models.CharField(max_length=15)
    company = models.ForeignKey(Company)
    reviewer = models.ForeignKey(Reviewer)
    client = models.ForeignKey(Client)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-pk']
