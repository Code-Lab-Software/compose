from django.apps import apps
from django.db import models

class ControllerType(models.Model):
    app_label = models.CharField(max_length=127)
    model = models.CharField(max_length=127)

    def get_app_config(self):
        return apps.get_app_config(self.app_label)

    def get_model(self):
        return apps.get_model(self.app_label, self.model)

class Controller(models.Model):
    controller_type = models.ForeignKey('ControllerType', related_name='controllers')
    name = models.CharField(max_length=128)

    def get_controller_object(self):
        return self.controller_type.get_model().objects.get(name=self.name)

    class Meta:
        unique_together = (('name', 'controller_type'),)

    
