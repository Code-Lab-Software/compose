import inspect

from django.apps import apps
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import post_save

CONTROLLER_CLASSES = ['Controller', 'ControllerStateArgument', 'ControllerState', 'ControllerStateArgumentProvider']

def register_on_post_save(sender, instance, created, raw, using, **kwargs):
    instance.register_with_branch()

def is_controller(model):
    return ControllerBase.is_controller(model)
    
def get_controller_class(bases):
    # Create a set object out of CONTROLLER_CLASSES list. We will use
    # it to check wich `Controller*` class is in the creation process
    controller_classes_set = set(CONTROLLER_CLASSES)
    controller_classes_intersection = controller_classes_set.intersection(set([base.__name__ for base in bases]))
    # Now check, whether the intersetion is len == 1 object
    if len(controller_classes_intersection) > 1:
        # We raise exception here - it's not allowed
        # for the classes to have more than one `Controller*`
        # as parent class
        raise TypeError(
                        "Controller subclass can use only one Controller* superclass."
                        "Now it is using '%s'." % controller_classes_intersection
                    )
    elif len(controller_classes_intersection) == 1:
        # Let's get and return the class name
        return controller_classes_intersection.pop()
    return None

# -------------------------------------------------------
# Controller
# -------------------------------------------------------
class ControllerTracker(ModelBase):
    def __new__(cls, name, bases, attrs):
        _new = super(ControllerTracker, cls).__new__(cls, name, bases, attrs)
        # Register the controller subclass first. `get_controller_class`
        # may throw TypeError exception if the `bases` contains more than
        # one base controller class, but that's OKay - if there's inproper
        # subclasses set we don't want to have class created
        controller_class_name = get_controller_class(bases)
        if not controller_class_name is None:
            # and then, we can rerieve the class object itself
            # from the module globals().
            globals()[controller_class_name].register_model(_new)
        return _new


# -------------------------------------------------------
# ControllerBase
# -------------------------------------------------------
    
class ControllerBase(models.Model):
    __metaclass__ = ControllerTracker
    __models_registry = {}

    @classmethod
    def register_model(cls, mdl):
        controller_class = cls.__name__.lower()
        if not cls.__models_registry.has_key(mdl._meta.app_label):
            cls.__models_registry[mdl._meta.app_label] = {'controller': None, 'states': {}, 'argument_providers': []}
        if cls.__models_registry.has_key(mdl._meta.app_label) and not cls.__models_registry[mdl._meta.app_label].has_key(mdl._meta.object_name):
            print 'Registering %s: %s' % (controller_class, mdl)
            # Now delegate the registry update to the proper subclass
            cls.update_registry(mdl, cls.__models_registry)
            # And in the end connect the post_save handler
            post_save.connect(register_on_post_save, sender=mdl)

    @classmethod
    def update_registry(cls, mdl, registry):
        raise NotImplementedError('`update_registry` class method have to be implemented in ControllerBase derived classes.')

    def get_scopes_type_model(self):
        models_map = {'Conroller': 'NodeType', 'ControllerArgument': 'NodeArgumentType', 'ControllerState': 'NodeStateType'}
        return apps.get_model('scopes.%s' % models_map.get(self.__class__.name))

    def get_scopes_entity_model(self):
        models_map = {'Controller': 'Node', 'ControllerStateArgument': 'NodeStateArgument', 'ControllerState': 'NodeState'}
        # Below we should call some 'get_controller_type' method instead of a complicated __models_registry lookup
        return apps.get_model('scopes.%s' % models_map.get(ControllerBase.__models_registry[self._meta.app_label][self._meta.object_name].__name__))

    @classmethod
    def is_controller(cls, model):
        return ControllerBase.__models_registry.has_key(model._meta.app_label)
    
    def register_scopes_type(self):
        return self.get_scopes_type_model().objects.register_for_entity(self)        
    
    def register_scopes_entity(self):
        return self.get_scopes_entity_model().objects.register_for_entity(self)        

    def register_with_branch(self):
        scopes_entity = self.register_scopes_entity()
        self.connect_with_scopes_entity(scopes_entity)
        return scopes_entity

    class Meta:
        abstract = True

class ControllerAttributeMixin(object):
    
    def get_controller(self):
        # It is assumed, that by default the controller argument
        # points to it's parent through the `controller`
        # attribute. The subclasses can override it, though.
        return self.controller
        
# -------------------------------------------------------
# Controller
# -------------------------------------------------------

class Controller(ControllerBase):
    branch = models.ForeignKey('scopes.Branch')
    node = models.OneToOneField('scopes.Node', null=True, editable=False)
    name = models.SlugField(max_length=128, unique=True)
    # Verbose information
    verbose_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    @classmethod
    def update_registry(cls, mdl, registry):
        registry[mdl._meta.app_label]['controller'] = mdl
        registry[mdl._meta.app_label][mdl._meta.object_name] = Controller
        
    def connect_with_scopes_entity(self, node):
        self.node = node
        self.save()
        
    class Meta:
        abstract = True
   
# -------------------------------------------------------
# ControllerStateArgument
# -------------------------------------------------------

class ControllerStateArgument(ControllerBase, ControllerAttributeMixin):
    name = models.SlugField()
    node_state_argument = models.OneToOneField('scopes.NodeStateArgument', null=True, editable=False)
    
    @classmethod
    def update_registry(cls, mdl, registry):
        state_mdl = mdl._meta.get_field_by_name('state')[0].related_model
        if registry[mdl._meta.app_label]['states'].has_key(state_mdl):
            registry[mdl._meta.app_label]['states'][state_mdl].append(mdl)
        else:
            registry[mdl._meta.app_label]['states'][state_mdl] = [mdl]
        registry[mdl._meta.app_label][mdl._meta.object_name] = ControllerStateArgument
    
    def connect_with_scopes_entity(self, node_state_argument):
        self.node_state_argument = node_state_argument
        self.save()
   
    class Meta:
        abstract = True
        # It's assumed here, that relation to the parent state object
        # is provided with the 'state' ForeignKey or
        # OneToOneField. But it would be better to handle the name of the attribute
        # dynamically. 
        unique_together = (('name', 'state'),)

# -------------------------------------------------------
# ControllerState
# -------------------------------------------------------

class ControllerState(ControllerBase, ControllerAttributeMixin):
    name = models.SlugField()
    node_state = models.OneToOneField('scopes.NodeState', null=True, editable=False)

    @classmethod
    def update_registry(cls, mdl, registry):
        if not registry[mdl._meta.app_label]['states'].has_key(mdl):
            registry[mdl._meta.app_label]['states'] = {mdl: []}
        registry[mdl._meta.app_label][mdl._meta.object_name] = ControllerState
    
    def connect_with_scopes_entity(self, node_state):
        self.node_state = node_state
        self.save()
   
    def get(self):
        raise NotImplementedError('get() method has to to be implemented in ControllerState derived classes.')
        
    class Meta:
        abstract = True
        # Same story with the `controller` key as in the `unique_together`
        # in ControllerArgument class
        unique_together = (('name', 'controller'),)


# -------------------------------------------------------
# ControllerStateArgumentProvider
# -------------------------------------------------------

class ControllerStateArgumentProvider(ControllerBase, ControllerAttributeMixin):
    name = models.SlugField()
    node_state_argument = models.OneToOneField('scopes.NodeStateArgument')
    node_state_argument_provider = models.OneToOneField('scopes.NodeStateArgumentProvider', null=True, editable=False)

    @classmethod
    def update_registry(cls, mdl, registry):
        registry[mdl._meta.app_label]['argument_providers'].appen(mdl)
        registry[mdl._meta.app_label][mdl._meta.object_name] = ControllerStateArgumentProvider
    
    def connect_with_scopes_entity(self, node_state_argument_provider):
        self.node_state_argument_provider = node_state_argument_provider
        self.save()
   
    class Meta:
        abstract = True

