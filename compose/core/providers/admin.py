from django.contrib import admin
from .models import ResourceStateArgumentProvider, NodeStateArgumentProvider

@admin.register(ResourceStateArgumentProvider, NodeStateArgumentProvider)
class ProvidersAdmin(admin.ModelAdmin):
    pass
