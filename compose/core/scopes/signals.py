from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver

@receiver(post_save, sender='scopes.Resource')
def register_resource_scope(sender, instance, created, raw, using, **kwargs):
    if created:
        apps.get_model('scopes.Scope').objects.register_for_resource(instance)

