from django.db import models


class BranchArgumentProvider(models.Model):

    branch_argument = models.OneToOneFieldy('scopes.BranchArgument', related_name='provider')
    node_state = models.OneToOneField('scopes.NodeState', related_name='provider')


class NodeArgumentProvider(models.Model):

    branch_argument = models.ForeignKey('scopes.BranchArgument', related_name='providers')
    node_argument = models.OneToOneField('scopes.NodeArgument', related_name='provider')
