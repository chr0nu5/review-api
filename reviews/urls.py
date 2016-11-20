from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^companies/', views.companies),
    url(r'^reviewers/', views.reviewers),
]
