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


class NodeStateArgumentTypeManager(models.Manager):

    def register_for_entity(self, entity):
        node_type = NodeType.objects.register_for_entity(entity.get_controller())
        argument_type, created = self.get_or_create(node_type=node_type,
                                                    model_name=entity._meta.object_name.lower())
        return argument_type


class NodeStateArgumentType(models.Model):
    node_type = models.ForeignKey('scopes.NodeType')
    model_name = models.CharField(max_length=127)

    objects = NodeStateArgumentTypeManager()

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

        
class NodeStateArgumentProviderTypeManager(models.Manager):

    def register_for_entity(self, entity):
        node_state_argument_provider_type, created = self.get_or_create(app_label=entity._meta.app_label,
                                                 model_name=entity._meta.object_name.lower())
        return node_state_argument_provider_type
        
class NodeStateArgumentProviderType(models.Model):

    app_label = models.CharField(max_length=127)
    model_name = models.CharField(max_length=127)

    objects = NodeStateArgumentProviderTypeManager()

    def get_model(self):
        return apps.get_model(self.app_label, self.model_name)

    class Meta:
        unique_together = (('app_label', 'model_name'),)

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
    node_type = models.ForeignKey('scopes.NodeType', related_name='nodes')
    src_id = models.PositiveIntegerField()

    objects = NodeManager()

    def get_required_nodes(self):
        node_ids = get_model('providers','NoteStateArgumentProvider').objects.filter(node_state__node=self).value_list('node_state_argument__node_state__node', flat=True)
        return self.__class__.objects.filter(id__in=node_ids)

    def get_object(self):
        return self.node_type.get_model().objects.get(id=self.src_id)

    def get(self, **kwargs):
        data = {}
        for state in self.states.all():
            data[state.get_object().name] = state.get(**kwargs)
        return data
        
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
    node_state_type = models.ForeignKey('scopes.NodeStateType', related_name='states')
    src_id = models.PositiveIntegerField()

    objects = NodeStateManager()

    def get_object(self):
        return self.node_state_type.get_model().objects.get(id=self.src_id)

    def get(self, **kwargs):
        arguments_values = {}
        for argument in self.arguments.all():
            arguments_values[argument.get_object().name] = kwargs.get(argument.get_object().name, None)
            
        return self.get_object().get(**arguments_values)
        
    class Meta:
        unique_together = (('node_state_type', 'src_id'),)


class NodeStateArgumentManager(models.Manager):

    def register_for_entity(self, entity):
        node_state = entity.state.node_state
        node_state_argument_type = NodeStateArgumentType.objects.register_for_entity(entity)
        node_state_argument, created = self.get_or_create(node_state=node_state, node_state_argument_type=node_state_argument_type, src_id=entity.pk)
        return node_state_argument
        
class NodeStateArgument(models.Model):
    node_state = models.ForeignKey('scopes.NodeState', related_name='arguments')
    node_state_argument_type = models.ForeignKey('scopes.NodeStateArgumentType', related_name='arguments')
    src_id = models.PositiveIntegerField()

    objects = NodeStateArgumentManager()

    def get_object(self):
        return self.node_state_argument_type.get_model().objects.get(id=self.src_id)
    
    class Meta:
        unique_together = (('node_state_argument_type', 'src_id'),)

class NodeStateArgumentProviderManager(models.Manager):

    def register_for_entity(self, entity):
        node_state_argument_provider_type = NodeStateArgumentProviderType.objects.register_for_entity(entity)
        node_state_argument_provider, created = self.get_or_create(node_state_argument=entity.node_state_argument, node_state_argument_provider_type=node_state_argument_provider_type, src_id=entity.pk)
        return node_state_argument_provider


class NodeStateArgumentProvider(models.Model):
    node_state_argument = models.ForeignKey('scopes.NodeStateArgument', related_name='providers')
    node_state_argument_provider_type = models.ForeignKey('scopes.NodeStateArgumentProviderType', related_name='providers')
    src_id = models.PositiveIntegerField()

    objects = NodeStateArgumentProviderManager()

    def get_object(self):
        return self.node_state_argument_provider_type.get_model().objects.get(id=self.src_id)
    
    class Meta:
        unique_together = (('node_state_argument_provider_type', 'src_id'),)


    
