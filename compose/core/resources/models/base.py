from django.db import models

class ResourceBase(models.Model):

    class Meta:
        abstract = True

class ResourceArgumentBase(models.Model):

    class Meta:
        abstract = True

