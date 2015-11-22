from django.db import models


class Resource(models.Model):
    branch = models.OneToOneField('scopes.Branch')
    name = models.SlugField(max_length=128, unique=True)
    verbose_name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.verbose_name
    
    class Meta:
        verbose_name = u'Resource'


class ResourceArgument(models.Model):
    resource = models.ForeignKey('Resource')
    name = models.SlugField(max_length=128)
    regex = models.CharField(max_length=255)
    weight = models.IntegerField()
    
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.regex)

    class Meta:
        ordering = ('resource', 'weight', 'name')
        unique_together = ('resource', 'name')
        verbose_name = u'Resource argument'
