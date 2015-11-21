# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='verbose_name',
            field=models.CharField(default='', unique=True, max_length=255),
            preserve_default=False,
        ),
    ]
