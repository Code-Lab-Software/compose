from django.apps import apps
from django.db import models

class ScopeManager(models.Manager):

    def register_for_resource(self, resource):
        return self.create(resource=resource)

class Scope(models.Model):
    resource = models.OneToOneField('scopes.Resource')
    objects = ScopeManager()

    class Meta:
        ordering = ('resource__name', )
        verbose_name_plural = "Scopes"
