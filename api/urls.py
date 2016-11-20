from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^oauth/', include('oauth.urls')),
    url(r'^reviews/', include('reviews.urls')),
]
