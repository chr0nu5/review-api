from __future__ import unicode_literals

from django.db import models
from django.db.models import Avg

# Create your models here.
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

# Create your models here.
class Reviewer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Reviewer"
        verbose_name_plural = "Reviewers"
        ordering = ['-pk']

class Review(models.Model):
    rating = models.IntegerField()
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=10000)
    ip = models.CharField(max_length=15)
    company = models.ForeignKey(Company)
    reviewer = models.ForeignKey(Reviewer)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-pk']
