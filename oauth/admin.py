from django.contrib import admin
from .models import Client

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)

# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    fields = ('username', 'password')
    list_display = ('username', 'token', 'date_joined')

admin.site.register(Client,ClientAdmin)
