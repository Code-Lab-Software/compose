from django.conf import settings
from django.db import models

class ComposeBaseModel(models.Model):
    compose_id = models.CharField(max_length=63, verbose_name='Compose identifier', default=getattr(settings, 'COMPOSE_ID', ''), editable=False )

    class Meta:
        abstract = True
