from django.contrib import admin
from .models import Resource, Scope

@admin.register(Resource, Scope)
class ScopesAdmin(admin.ModelAdmin):
    pass
