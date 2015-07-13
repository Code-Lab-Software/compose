# -*- coding: utf-8 -*-
from django.conf import settings
import inspect

# te liste trzeba stopniowy zredukowac i zostawic tylko dziedziczenie po COmposeBasemodl
compose_apps = ('components', 'flags', 'formstyle', 'menu', 'pdfgen', 'prospects', 'records', 'fieldwidgets')

def is_compose_model(model):
    return model._meta.app_label in compose_apps or 'ComposeBaseModel' in (cls.__name__ for cls in inspect.getmro(model))

def is_compose_object(obj):
    return is_compose_model(obj.__class__)

class ComposeRouter(object):
    def db_for_read(self, model, **hints):
        if is_compose_model(model):
            return getattr(settings, 'DATABASES_MAP').get('compose')
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        if is_compose_object(obj1) and is_compose_object(obj2):
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == getattr(settings, 'DATABASES_MAP').get('compose'):
            return is_compose_model(model)
        elif is_compose_model(model):
            return False
        return None
