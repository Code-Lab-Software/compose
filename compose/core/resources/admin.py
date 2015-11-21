from django.contrib import admin
from .models import Resource, ResourceArgument

@admin.register(Resource, ResourceArgument)
class ResourcesAdmin(admin.ModelAdmin):
    pass
