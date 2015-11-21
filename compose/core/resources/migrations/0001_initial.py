# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scopes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(unique=True, max_length=128)),
                ('verbose_name', models.CharField(unique=True, max_length=255)),
                ('branch', models.OneToOneField(to='scopes.Branch')),
            ],
            options={
                'verbose_name': 'Resource',
            },
        ),
        migrations.CreateModel(
            name='ResourceArgument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(max_length=128)),
                ('regex', models.CharField(max_length=255)),
                ('weight', models.IntegerField()),
                ('resource', models.ForeignKey(to='resources.Resource')),
            ],
            options={
                'verbose_name': 'Resource argument',
            },
        ),
        migrations.AlterUniqueTogether(
            name='resourceargument',
            unique_together=set([('resource', 'name')]),
        ),
    ]
