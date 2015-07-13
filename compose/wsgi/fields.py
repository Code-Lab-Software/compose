from django.conf import settings
from django.db import models
from django.utils.encoding import smart_unicode, smart_str 
from django.contrib.contenttypes.generic import GenericForeignKey
from django.core.exceptions import ObjectDoesNotExist

models_with_external = ('CustomContentFlag',)
models_with_internal = ('LayoutItem', 'SizerItem', 'ListRepresentation')
compose_apps = ('formstyle', 'menu', 'prospects', 'records')
DEFAULT_DB, COMPOSE_DB = (getattr(settings, 'DATABASES_MAP').get(db) for db in ('default', 'compose'))

class CTDescriptor(property):

    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            return self
    
        if self.field.name not in instance.__dict__:
            # The object has not been created yet, so unpickle the data
            raw_data = getattr(instance, self.field.attname)
            # bez ztr jest type_error
            instance.__dict__[smart_str(self.field.name)] = self.field.get_ct(raw_data)
        return instance.__dict__[smart_str(self.field.name)]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value
        setattr(instance, self.field.attname, value)

class GenericContentType(models.CharField):

    def get_ct(self, model_path):
        if not model_path:
            return None
        app_label, model_name = model_path.split('.')
        return models.get_model('contenttypes', 'ContentType').objects.get(app_label=app_label, model=model_name)

    def get_attname(self):
        return "%s_path" % self.name
    
    def contribute_to_class(self, cls, name):
        super(GenericContentType, self).contribute_to_class(cls, name)
        setattr(cls, name, CTDescriptor(self))
        

class CTForeignKey(GenericForeignKey):
    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self
        try:
            return getattr(instance, self.cache_attr)
        except AttributeError:
            rel_obj = None

            f = self.model._meta.get_field(self.ct_field)
            ct_id = getattr(instance, self.fk_field)
            if ct_id:
                ct = getattr(instance, self.ct_field)
                try:
                    # making query thouth router
                    # we assume that there is only one database with data named 'default'
                    if self.model._meta.object_name in models_with_external:
                        rel_obj = ct.model_class().objects.get(pk=getattr(instance, self.fk_field))
                    else:
                        rel_obj = ct.model_class().objects.using(COMPOSE_DB).get(pk=getattr(instance, self.fk_field))
                except ObjectDoesNotExist:
                    pass
            setattr(instance, self.cache_attr, rel_obj)
            return rel_obj        

    def _check_content_type_field(self):
        return []
