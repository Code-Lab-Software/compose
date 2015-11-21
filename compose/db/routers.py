# -*- coding: utf-8 -*-
import inspect

from django.conf import settings
from compose.core.scopes.models import is_controller

COMPOSE_APPS = (
    'scopes',
    'resources',
    'providers',
)

def is_compose_model(model):
    return (model._meta.app_label in COMPOSE_APPS) or is_controller(model)

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

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if hints.get('model'):
            if db == getattr(settings, 'DATABASES_MAP').get('compose'):
                return is_compose_model(hints.get('model'))
            elif is_compose_model(hints.get('model')):
                return False
        return None
