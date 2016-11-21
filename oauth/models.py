from __future__ import unicode_literals

import uuid

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User


# encode user password
def after_save_client(sender, instance, **kwargs):
    user = sender.objects.get(username=instance.username)
    if len(instance.password) < 50:
        user.set_password(instance.password)
        user.save()


# Create your models here.
class Client(User):
    token = models.CharField(max_length=100, null=True, blank=True, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def generate_token(self):
        self.token = str(uuid.uuid4())

    def invalidate_token(self):
        self.token = None

    def get_token(self):
        return self.token


signals.post_save.connect(after_save_client, sender=Client)
