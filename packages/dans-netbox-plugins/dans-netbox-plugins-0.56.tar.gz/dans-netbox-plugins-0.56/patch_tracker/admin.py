# importing Django admin and our own database schema
from django.contrib import admin
from .models import Patch

@admin.register(Patch)
class PatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag')