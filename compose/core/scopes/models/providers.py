from django.db.models import Model

class BranchArgumentProvider(Model):

    branch_argument = models.OneToOneFieldy('scopes.BranchArgument', related_name='provider')
    node_state = models.OneToOneField('scopes.NodeState', related_name='provider')
    
class NodeArgumentProvider(Model):

    branch_argument = models.ForeignKey('scopes.BranchArgument', related_name='providers')
    node_argument = models.OneToOneField('scopes.NodeArgument', related_name='provider')

