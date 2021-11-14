# search_app/admin.py

from django.contrib import admin
from .models import Fashion

# Register your models here.

class FashionAdmin(admin.ModelAdmin):
    list_display = ()

admin.site.register(Fashion, FashionAdmin)