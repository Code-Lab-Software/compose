from django.apps import apps
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

class NodeTypeManager(models.Manager):

    def register_for_entity(self, entity):
        node_type, created = self.get_or_create(app_label=entity._meta.app_label,
                                                model_name=entity._meta.object_name.lower())
        return node_type
    

class NodeType(models.Model):
    app_label = models.CharField(max_length=127)
    model_name = models.CharField(max_length=127)

    objects = NodeTypeManager()

    def get_app_config(self):
        return apps.get_app_config(self.app_label)

    def get_model(self):
        return apps.get_model(self.app_label, self.model_name)

    class Meta:
        unique_together = (('app_label', 'model_name'),)


class NodeArgumentTypeManager(models.Manager):

    def register_for_entity(self, entity):
        node_type = NodeType.objects.register_for_entity(entity.get_controller())
        argument_type, created = self.get_or_create(node_type=node_type,
                                                    model_name=entity._meta.object_name.lower())
        return argument_type


class NodeArgumentType(models.Model):
    node_type = models.ForeignKey('scopes.NodeType')
    model_name = models.CharField(max_length=127)

    objects = NodeArgumentTypeManager()

    def get_model(self):
        return apps.get_model(self.node_type.app_label, self.model_name)
    
    class Meta:
        unique_together = (('node_type', 'model_name'),)

class NodeStateTypeManager(models.Manager):

    def register_for_entity(self, entity):
        node_type = NodeType.objects.register_for_entity(entity.get_controller())
        state_type, created = self.get_or_create(node_type=node_type,
                                                 model_name=entity._meta.object_name.lower())
        return state_type
        
class NodeStateType(models.Model):
    node_type = models.ForeignKey('scopes.NodeType')
    model_name = models.CharField(max_length=127)

    objects = NodeStateTypeManager()

    def get_model(self):
        return apps.get_model(self.node_type.app_label, self.model_name)

    class Meta:
        unique_together = (('node_type', 'model_name'),)

# -----------------------------------------------
# Objects registry
# -----------------------------------------------

class NodeManager(models.Manager):

    def register_for_entity(self, entity):
        node_type = apps.get_model('scopes', 'NodeType').objects.register_for_entity(entity)
        node, created = self.get_or_create(branch=entity.branch, node_type=node_type, src_id=entity.pk)
        return node


class Node(models.Model):
    branch = models.ForeignKey('scopes.Branch', related_name='nodes')
    node_type = models.ForeignKey('NodeType', related_name='nodes')
    src_id = models.PositiveIntegerField()

    objects = NodeManager()

    def get_required_nodes(self):
       return self.__class__.objects.filter(states__provider__branch_argument__providers__node_argument__node=self)

    def get_object(self):
        return self.node_type.get_model().objects.get(id=self.src_id)

    class Meta:
        unique_together = (('node_type', 'src_id'),)


class NodeStateManager(models.Manager):

    def register_for_entity(self, entity):
        node = Node.objects.register_for_entity(entity.get_controller())
        node_state_type = NodeStateType.objects.register_for_entity(entity)
        node_state, created = self.get_or_create(node=node, node_state_type=node_state_type, src_id=entity.pk)
        return node_state

    
class NodeState(models.Model):
    node = models.ForeignKey('scopes.Node', related_name='states')
    node_state_type = models.ForeignKey('NodeStateType', related_name='states')
    src_id = models.PositiveIntegerField()

    objects = NodeStateManager()

    def get_object(self):
        return self.node_state_type.get_model().objects.get(id=self.src_id)

    class Meta:
        unique_together = (('node_state_type', 'src_id'),)


class NodeArgumentManager(models.Manager):

    def register_for_entity(self, entity):
        node = Node.objects.register_for_entity(entity.get_controller())
        node_argument_type = NodeArgumentType.objects.register_for_entity(entity)
        node_argument, created = self.get_or_create(node=node, node_argument_type=node_argument_type, src_id=entity.pk)
        return node_argument
        
class NodeArgument(models.Model):
    node = models.ForeignKey('scopes.Node', related_name='arguments')
    node_argument_type = models.ForeignKey('NodeArgumentType', related_name='arguments')
    src_id = models.PositiveIntegerField()

    objects = NodeArgumentManager()

    def get_object(self):
        return self.node_argument_type.get_model().objects.get(id=self.src_id)
    
    class Meta:
        unique_together = (('node_argument_type', 'src_id'),)




    
