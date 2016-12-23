from django.contrib import admin
from .models import Resource, Scope, Identifier

@admin.register(Resource, Scope, Identifier)
class ScopesAdmin(admin.ModelAdmin):
    pass
