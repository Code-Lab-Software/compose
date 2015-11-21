from django.db import models
from compose.core.scopes.models import ControllerStateArgumentProvider


class ResourceStateArgumentProvider(ControllerStateArgumentProvider):
    resource_argument = models.ForeignKey('resources.ResourceArgument')
    
    class Meta:
        verbose_name = u'Resource state argument provider'

class NoteStateArgumentProvider(ControllerStateArgumentProvider):
    node_state = models.ForeignKey('scopes.NodeState')
    
    class Meta:
        verbose_name = u'Note state argument provider'
        verbose_name_plural = u'Note state argument providers'
        