from django.db import models

def build_node_dependency_list(node, dependency_list=[]):
    if node in dependency_list:
        return
    required_nodes = node.get_required_nodes()
    for r_node in required_nodes:
        if not r_node in dependency_list:
            build_node_dependency_list(r_node, dependency_list)
    dependency_list.append(node)

# -----------------------------------------------
# Types registry
# -----------------------------------------------

class NodeType(models.Model):
    app_label = models.CharField(max_length=127)
    model_name = models.CharField(max_length=127)

    def get_app_config(self):
        return apps.get_app_config(self.app_label)

    def get_model(self):
        return apps.get_model(self.app_label, self.model_name)

    class Meta:
        unique_together = (('app_label', 'model_name'),)

class NodeArgumentType(models.Model):
    node_type = models.ForeignKey('scopes.NodeType')
    model_name = models.CharField(max_length=127)

    def get_model(self):
        return apps.get_model(self.node_type.app_label, self.model_name)
    
    class Meta:
        unique_together = (('node_type', 'model_name'),)
    
class NodeStateType(models.Model):
    node_type = models.ForeignKey('scopes.NodeType')
    model_name = models.CharField(max_length=127)

    def get_model(self):
        return apps.get_model(self.node_type.app_label, self.model_name)

    class Meta:
        unique_together = (('node_type', 'model_name'),)

# -----------------------------------------------
# Objects registry
# -----------------------------------------------
    
class Node(models.Model):
    branch = models.ForeignKey('scopes.Branch', related_name='nodes')
    node_type = models.ForeignKey('NodeType', related_name='nodes')
    src_id = models.PositiveIntegerField()

    def get_required_nodes(self):
       return self.__class__.objects.filter(states__provider__branch_argument__providers__node_argument__node=self)

    def get_object(self):
        return self.node_type.get_model().objects.get(id=self.src_id)

    class Meta:
        unique_together = (('node_type', 'src_id'),)

class NodeState(models.Model):
    node = models.ForeignKey('scopes.Node', related_name='states')
    node_state_type = models.ForeignKey('NodeStateType', related_name='states')
    src_id = models.PositiveIntegerField()

    def get_object(self):
        return self.node_state_type.get_model().objects.get(id=self.src_id)

    class Meta:
        unique_together = (('node_state_type', 'src_id'),)

class NodeArgument(models.Model):
    node = models.ForeignKey('scopes.Node', related_name='arguments')
    node_argument_type = models.ForeignKey('NodeArgumentType', related_name='arguments')
    src_id = models.PositiveIntegerField()

    def get_object(self):
        return self.node_argument_type.get_model().objects.get(id=self.src_id)
    
    class Meta:
        unique_together = (('node_argument_type', 'src_id'),)




    
