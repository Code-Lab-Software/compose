from django.apps import apps
from django.db import models


class EntityTypeBase(models.Model):
    pass


class EntityType(models.Model):
    app_label = models.CharField(max_length=127)
    model = models.CharField(max_length=127)

    def get_app_config(self):
        return apps.get_app_config(self.app_label)

    def get_model(self):
        return apps.get_model(self.app_label, self.model)


class Entity(models.Model):
    entity_type = models.ForeignKey('EntityType', related_name='entities')
    entity_id = models.PositiveIntegerField()

    def get_entity_object(self):
        return self.entity_type.get_model().objects.get(id=self.entity_id)
