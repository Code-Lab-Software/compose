from django.db import models

class ThemeType(models.Model):
    app_label = models.CharField(max_length=127)
    model_name = models.CharField(max_length=127)

class Theme(models.Model):
    theme_type = models.ForeignKey('resources.ThemeType', related_name='themes')
    src_id = models.PositiveIntegerField()

class ThemeBase(models.Model):
    theme = models.OneToOneField('resources.Theme')

    def get_template_name(self):
        raise NotImplenetedError

    class Meta:
        abstract = True


