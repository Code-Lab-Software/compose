from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import post_save

# -------------------------------------------------------
# Meta-stuff
# -------------------------------------------------------
class EntityTypeTracker(ModelBase):
    def __new__(cls, name, bases, attrs):
        _new = super(EntityTypeTracker, cls).__new__(cls, name, bases, attrs)
        try:
            if EntityTypeBase not in bases:
                return _new
        except NameError:
            return _new
        else:
            EntityTypeBase.register_model(_new)
        return _new


class EntityTypeBase(models.Model):
    __metaclass__ = EntityTypeTracker
    _entity_models = []

    @classmethod
    def register_model(cls, mdl):
        cls._entity_models.append(mdl)
        post_save.connect(notify_on_post_save, sender=mdl)
    
    class Meta:
        abstract = True

def notify_on_post_save(sender, instance, created, raw, using, **kwargs):
    pass


    


    
