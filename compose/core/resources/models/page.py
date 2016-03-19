from django.db import models

class Page(models.Model):
    resource = models.OneToOneField('resources.HttpResource')
    theme = models.ForeignKey('resources.theme')

class Region(models.Model):
    name = models.CharField(max_lenth=255)
    page = models.ForeignKey('scopes.Page')
    renderer = models.ForeignKey('scopes.RegionRenderer')
    weight = models.IntegerField()

class RegionItem(models.Model):
    region = models.ForeignKey('scopes.Region')
    item_type = models.CharField(max_length=1, choices=(('r', 'Region'), ('n', 'Node')))
    item_id = models.PositiveSmallIntegerField()
    weight = models.IntegerField()
    proportion = models.PositiveSmallIntegerField()


class RegionRendererType(models.Model):
    app_label = models.CharField(max_length=127)
    model_name = models.CharField(max_length=127)

   
class RegionRenderer(models.Model):
    renderer_type = models.ForeignKey('scopes.RegionRendererType')
    renderer_id = models.PositiveIntegerField()


class NodeRendererType(models.Model):
    app_label = models.CharField(max_length=127)
    model_name = models.CharField(max_length=127)

   
class NodeRenderer(models.Model):
    renderer_type = models.ForeignKey('scopes.NodeRendererType')
    renderer_id = models.PositiveIntegerField()


    
