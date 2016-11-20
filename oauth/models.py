from __future__ import unicode_literals

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User

# encode user password
def after_save_client(sender, instance, **kwargs):
    user = sender.objects.get(username=instance.username)
    if len(instance.password)<50:
        user.set_password(instance.password)
        user.save()

# Create your models here.
class Client(User):
    token = models.CharField(max_length=100, null=True, blank=True, unique=True)
    def __unicode__(self):
        return self.first_name

signals.post_save.connect(after_save_client, sender=Client)
