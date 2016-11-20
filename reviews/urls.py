from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^get_companies/', views.get_companies),
]
