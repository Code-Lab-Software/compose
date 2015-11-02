import inspect

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import post_save

CONTROLLER_CLASSES = ['Controller', 'ControllerArgument', 'ControllerState']

def register_on_post_save(sender, instance, created, raw, using, **kwargs):
    instance.register_with_branch()

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
        print 'Registering %s: %s' % (controller_class, mdl)
        if not cls.__models_registry.has_key(mdl._meta.app_label):
            cls.__models_registry[mdl._meta.app_label] = {'controller': None, 'states': [], 'arguments': []}
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
        models_map = {'Conroller': 'Node', 'ControllerArgument': 'NodeArgument', 'ControllerState': 'NodeState'}
        return apps.get_model('scopes.%s' % models_map.get(self.__class__.name))
    
    def register_scopes_type(self):
        return self.get_scopes_type_model().objects.register_for_controller(self)        
    
    def register_scopes_entity(self):
        return self.get_scopes_entity_model().objects.register_for_controller(self)        

    def register_with_branch():
        return self.register_scopes_entity()

    class Meta:
        abstract = True

    
# -------------------------------------------------------
# Controller
# -------------------------------------------------------

class Controller(ControllerBase):
    branch = models.ForeignKey('scopes.Branch')
    node = models.OneToOneField('scopes.Node', null=True)
    name = models.SlugField(max_length=128, unique=True)
    # Verbose information
    verbose_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    @classmethod
    def update_registry(cls, mdl, registry):
        registry[mdl._meta.app_label]['controller'] = mdl
        
    class Meta:
        abstract = True
   
# -------------------------------------------------------
# ControllerArgument
# -------------------------------------------------------

class ControllerArgument(ControllerBase):
    name = models.SlugField(unique=True)

    @classmethod
    def update_registry(cls, mdl, registry):
        registry[mdl._meta.app_label]['arguments'].append(mdl)
    
    class Meta:
        abstract = True

# -------------------------------------------------------
# ControllerState
# -------------------------------------------------------

class ControllerState(ControllerBase):
    name = models.SlugField(unique=True)

    @classmethod
    def update_registry(cls, mdl, registry):
        registry[mdl._meta.app_label]['states'].append(mdl)
    
    class Meta:
        abstract = True

    
