from django.db.models import Model

class Root(Model):
    name = models.SlugField(max_length=128, unique=True)
    verbose_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    
    class Meta:
        ordering = ('name',)
