from django.apps import apps
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Resource(models.Model):
    """Represents URI - together with the instances of Identifier model below, 
    instances of this model will enable usage of the following URL format:
    protocol://host/{{ name }}/{{ identifier-1 }}/{{ identifier-2 }}/.../{{ identifier-n }}
    """
    name = models.SlugField(max_length=128,
                            unique=True,
                            help_text=_('''Unique resource name. This will be used to build the URL as 
                                           a protocol://host/{{ name }}/.../'''))
    verbose_name = models.CharField(max_length=255,)
    description = models.TextField(blank=True,
                                   help_text=_('Optional descriptive memo here. What is this resource for, why was it created?'))
    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Resources"


class Identifier(models.Model):
    """Represents individual URI component as a regular expression. Also attaches the weight and the name
    so that the corresponding URL can be properly validated.
    """
    resource = models.ForeignKey('scopes.Resource', related_name='identifiers')
    weight = models.PositiveSmallIntegerField()
    name = models.SlugField(max_length=128)
    regex = models.SlugField(max_length=128)

    class Meta:
        ordering = ('resource__name', 'weight', 'name')
        unique_together = (('resource', 'name'), ('resource', 'weight'))
        verbose_name_plural = "Identifiers"
