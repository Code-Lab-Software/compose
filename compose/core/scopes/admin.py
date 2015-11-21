from django.contrib import admin
from .models import Root, Branch, Node, NodeStateArgument, NodeState, NodeType, NodeStateArgumentType, NodeStateType

@admin.register(Root, Branch, Node, NodeStateArgument, NodeState, NodeType, NodeStateArgumentType, NodeStateType)
class ScopesAdmin(admin.ModelAdmin):
    pass
