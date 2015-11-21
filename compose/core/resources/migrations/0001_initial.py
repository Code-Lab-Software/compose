# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scopes', '0002_auto_20151121_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(unique=True, max_length=128)),
                ('branch', models.OneToOneField(to='scopes.Branch')),
            ],
            options={
                'verbose_name': 'Resource',
                'verbose_name_plural': 'Resources',
            },
        ),
    ]
