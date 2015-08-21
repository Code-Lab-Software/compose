from django.db import models


def build_node_dependency_list(node, dependency_list=[]):
    if node in dependency_list:
        return
    required_nodes = node.get_required_nodes()
    for r_node in required_nodes:
        if not r_node in dependency_list:
            build_node_dependency_list(r_node, dependency_list)
    dependency_list.append(node)


class Node(models.Model):

    branch = models.ForeignKey('scopes.Branch', related_name='nodes')

    entity = models.ForeignKey('scopes.Entity', related_name='nodes')

    name = models.SlugField(max_length=128)
    verbose_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    weight = models.IntegerField()

    def get_required_nodes(self):
        return self.__class__.objects.filter(states__provider__branch_argument__providers__node_argument__node=self)

    class Meta:
        unique_together = (('branch', 'name'), ('branch', 'verbose_name'))
        ordering = ('weight',)


class NodeState(models.Model):

    node = models.ForeignKey('scopes.Node', related_name='states')


class NodeArgument(models.Model):

    node = models.ForeignKey('scopes.Node', related_name='arguments')

class NodeArgumentState(models.Model):

    node_argument = models.OneToOneField('scopes.NodeArgument', related_name='state')
    node_state = models.ForeignKey('scopes.NodeState', related_name='arguments')

    
