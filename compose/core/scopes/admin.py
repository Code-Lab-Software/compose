from django.contrib import admin
from .models import Root, Branch, Node, NodeArgument, NodeState, NodeType, NodeArgumentType, NodeStateType

@admin.register(Root, Branch, Node, NodeArgument, NodeState, NodeType, NodeArgumentType, NodeStateType)
class ScopesAdmin(admin.ModelAdmin):
    pass
