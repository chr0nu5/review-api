from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^token/', views.token),
    url(r'^invalidate_token/', views.invalidate_token),
]
