from django.db import models
from scopes.models import ControllerStateArgumentProvider


class ResourceStateArgumentProvider(ControllerStateArgumentProvider):
    resource_argument = models.ForeignKey('ResourceArgument')

    class Meta:
        verbose_name = u'Resource state argument provider'
