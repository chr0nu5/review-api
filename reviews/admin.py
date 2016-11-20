from django.contrib import admin
from .models import Company
from .models import Reviewer
from .models import Review

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer','company','rating','title','ip','created_date')
    search_fields = ('reviewer__name','title','ip')

class ReviewerAdmin(admin.ModelAdmin):
    list_display = ('name','email')
    search_fields = ('name','email')

admin.site.register(Company)
admin.site.register(Reviewer, ReviewerAdmin)
admin.site.register(Review, ReviewAdmin)
