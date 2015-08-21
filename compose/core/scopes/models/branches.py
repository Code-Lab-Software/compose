from compose.core.scopes.models.nodes import build_node_dependency_list
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Branch(models.Model):
    root = models.ForeignKey('scopes.Root', related_name='branches')
    name = models.SlugField(max_length=128, unique=True)
    verbose_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def build_nodes_dependency_list(self):
        nodes_dependency_list = []
        for node in self.nodes.all():
            build_nodes_dependency_list(node, nodes_dependency_list)
        return nodes_dependency_list

    class Meta:
        unique_together = (('branch', 'name'), ('branch', 'weight'))
        ordering = ('name',)


class BranchArgument(models.Model):
    branch = models.ForeignKey('scopes.Branch', related_name='arguments')
    name = models.SlugField(max_length=128)
    regex = models.CharField(max_length=255, help_text=_("Will validate this argument value fetched with `scopes.BranchArgumentProvider`"))
    weight = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        unique_together = (('branch', 'name'), ('branch', 'weight'))
        ordering = ('branch__name', 'weight',)
