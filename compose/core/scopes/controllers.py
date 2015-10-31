import inspect

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import post_save

CONTROLLER_CLASSES = ['Controller', 'ControllerArgument', 'ControllerState']

def register_on_post_save(sender, instance, created, raw, using, **kwargs):
    pass

def check_controller_type(bases):
    controller_classes_set = set(CONTROLLER_CLASSES)
    return controller_classes_set.intersection(set([base.__name__ for base in bases]))

# -------------------------------------------------------
# Controller
# -------------------------------------------------------
class ControllerTracker(ModelBase):
    def __new__(cls, name, bases, attrs):
        _new = super(ControllerTracker, cls).__new__(cls, name, bases, attrs)
        # Create a set object out of CONTROLLER_CLASSES list. We will use
        # it to check wich `Controller*` class is in the creation process
        controller_classes_intersection = check_controller_type(bases)
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
            # Let's get the class name
            controller_class = controller_classes_intersection.pop()
            # and then, we can rerieve the class object itself
            # from the module globals()... and finally register the controller
            # subclass
            globals()[controller_class].register_model(_new, controller_class)
        return _new


# -------------------------------------------------------
# ControllerBase
# -------------------------------------------------------
    
class ControllerBase(models.Model):
    __metaclass__ = ControllerTracker
    __models_registry = {}

    @classmethod
    def register_model(cls, mdl, controller_class):
        controller_class = controller_class.lower()
        print 'Registering %s: %s' % (controller_class, mdl)
        if not cls.__models_registry.has_key(mdl._meta.app_label):
            cls.__models_registry[mdl._meta.app_label] = {'controller': None, 'states': [], 'arguments': []}
        if controller_class == 'controller':
            cls.__models_registry[mdl._meta.app_label][controller_class] = mdl
        else:
            cls.__models_registry[mdl._meta.app_label]['%ss' % controller_class.replace('controller', '')].append(mdl)

        print cls.__models_registry
        post_save.connect(register_on_post_save, sender=mdl)

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
    
    class Meta:
        abstract = True
   
# -------------------------------------------------------
# ControllerArgument
# -------------------------------------------------------

class ControllerArgument(ControllerBase):
    name = models.SlugField(unique=True)

    class Meta:
        abstract = True

# -------------------------------------------------------
# ControllerState
# -------------------------------------------------------

class ControllerState(ControllerBase):
    name = models.SlugField(unique=True)

    class Meta:
        abstract = True

    
