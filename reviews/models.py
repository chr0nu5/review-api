from __future__ import unicode_literals

import re
import unidecode

from django.db import models
from django.db.models import Avg
from django.core.cache import cache
from django.core.exceptions import ValidationError

from oauth.models import Client


def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'\W+', '-', text)


def validate_rating(value):
    try:
        value = int(value)
        if value < 1 or value > 5:
            raise ValidationError('Rating should be between 1 and 5')
    except ValueError:
        raise ValidationError('Rating should be a valid integer')


def validate_summary(value):
    print len(value)
    if len(value) > 10000:
        raise ValidationError('Invalid summary')


class Company(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['-pk']

    def get_rating(self):
        key = "rating_%s_%s" % (str(self.pk), self.name)
        return cache.get(key)

    def update_average_rating(self):
        rating = Review.objects.filter(company=self).aggregate(Avg('rating'))['rating__avg']
        cache.set("rating_%s_%s" % (str(self.pk), self.name), rating)


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
