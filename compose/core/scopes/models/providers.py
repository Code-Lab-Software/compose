from django.db import models


class BranchArgumentState(models.Model):

    branch_argument = models.OneToOneFieldy('scopes.BranchArgument', related_name='state')
    node_state = models.OneToOneField('scopes.NodeState', related_name='branch_argument_state')


class NodeArgumentState(models.Model):

    node_argument = models.OneToOneField('scopes.NodeArgument', related_name='state')
    branch_argument_state = models.ForeignKey('scopes.BranchArgumentState', related_name='node_argument_state')

