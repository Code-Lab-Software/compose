# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import compose.core.scopes.models.controllers


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
        ('scopes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteStateArgumentProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField()),
                ('node_state', models.ForeignKey(to='scopes.NodeState')),
                ('node_state_argument', models.OneToOneField(to='scopes.NodeStateArgument')),
                ('node_state_argument_provider', models.OneToOneField(null=True, editable=False, to='scopes.NodeStateArgumentProvider')),
            ],
            options={
                'verbose_name': 'Note state argument provider',
                'verbose_name_plural': 'Note state argument providers',
            },
            bases=(models.Model, compose.core.scopes.models.controllers.ControllerAttributeMixin),
        ),
        migrations.CreateModel(
            name='ResourceStateArgumentProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField()),
                ('node_state_argument', models.OneToOneField(to='scopes.NodeStateArgument')),
                ('node_state_argument_provider', models.OneToOneField(null=True, editable=False, to='scopes.NodeStateArgumentProvider')),
                ('resource_argument', models.ForeignKey(to='resources.ResourceArgument')),
            ],
            options={
                'verbose_name': 'Resource state argument provider',
            },
            bases=(models.Model, compose.core.scopes.models.controllers.ControllerAttributeMixin),
        ),
    ]
