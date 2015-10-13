from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import post_save

CONTROLLER_CLASSES = ['Controller', 'ControllerArgument', 'ControllerState']

# -------------------------------------------------------
# Controller
# -------------------------------------------------------
class ControllerTracker(ModelBase):
    def __new__(cls, name, bases, attrs):
        _new = super(ControllerTracker, cls).__new__(cls, name, bases, attrs)
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
            # Let's get the class name
            controller_class = controller_classes_intersection.pop()
            # and then, we can rerieve the class object itself
            # from the module globals()... and finally register the controller
            # subclass
            globals()[controller_class].register_model(_new)
        return _new


# -------------------------------------------------------
# Controller
# -------------------------------------------------------
    
class Controller(models.Model):
    __metaclass__ = ControllerTracker
    __models_registry = {}

    name = models.SlugField(unique=True)

    class Meta:
        abstract = True
    
    @classmethod
    def register_model(cls, mdl):
        print 'Registering Controller class'
        # cls.__tracked_models.append(mdl)
        # post_save.connect(notify_on_post_save, sender=mdl)
        
def notify_on_post_save(sender, instance, created, raw, using, **kwargs):
    pass

# -------------------------------------------------------
# ControllerArgument
# -------------------------------------------------------

class ControllerArgument(models.Model):
    __metaclass__ = ControllerTracker
    
    name = models.SlugField(unique=True)

    @classmethod
    def register_model(cls, mdl):
        print 'Registering Argument subclass..'
    
    class Meta:
        abstract = True

# -------------------------------------------------------
# ControllerState
# -------------------------------------------------------

class ControllerState(models.Model):
    __metaclass__ = ControllerTracker
    
    name = models.SlugField(unique=True)

    @classmethod
    def register_model(cls, mdl):
        print 'Registering State subclass..'

    
    class Meta:
        abstract = True

    
