# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(unique=True, max_length=128)),
                ('verbose_name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('src_id', models.PositiveIntegerField()),
                ('branch', models.ForeignKey(related_name='nodes', to='scopes.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='NodeState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('src_id', models.PositiveIntegerField()),
                ('node', models.ForeignKey(related_name='states', to='scopes.Node')),
            ],
        ),
        migrations.CreateModel(
            name='NodeStateArgument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('src_id', models.PositiveIntegerField()),
                ('node_state', models.ForeignKey(related_name='arguments', to='scopes.NodeState')),
            ],
        ),
        migrations.CreateModel(
            name='NodeStateArgumentProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('src_id', models.PositiveIntegerField()),
                ('node_state_argument', models.ForeignKey(related_name='providers', to='scopes.NodeStateArgument')),
            ],
        ),
        migrations.CreateModel(
            name='NodeStateArgumentProviderType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_label', models.CharField(max_length=127)),
                ('model_name', models.CharField(max_length=127)),
            ],
        ),
        migrations.CreateModel(
            name='NodeStateArgumentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_name', models.CharField(max_length=127)),
            ],
        ),
        migrations.CreateModel(
            name='NodeStateType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_name', models.CharField(max_length=127)),
            ],
        ),
        migrations.CreateModel(
            name='NodeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_label', models.CharField(max_length=127)),
                ('model_name', models.CharField(max_length=127)),
            ],
        ),
        migrations.CreateModel(
            name='Root',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(unique=True, max_length=128)),
                ('verbose_name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='nodetype',
            unique_together=set([('app_label', 'model_name')]),
        ),
        migrations.AddField(
            model_name='nodestatetype',
            name='node_type',
            field=models.ForeignKey(to='scopes.NodeType'),
        ),
        migrations.AddField(
            model_name='nodestateargumenttype',
            name='node_type',
            field=models.ForeignKey(to='scopes.NodeType'),
        ),
        migrations.AlterUniqueTogether(
            name='nodestateargumentprovidertype',
            unique_together=set([('app_label', 'model_name')]),
        ),
        migrations.AddField(
            model_name='nodestateargumentprovider',
            name='node_state_argument_provider_type',
            field=models.ForeignKey(related_name='providers', to='scopes.NodeStateArgumentProviderType'),
        ),
        migrations.AddField(
            model_name='nodestateargument',
            name='node_state_argument_type',
            field=models.ForeignKey(related_name='arguments', to='scopes.NodeStateArgumentType'),
        ),
        migrations.AddField(
            model_name='nodestate',
            name='node_state_type',
            field=models.ForeignKey(related_name='states', to='scopes.NodeStateType'),
        ),
        migrations.AddField(
            model_name='node',
            name='node_type',
            field=models.ForeignKey(related_name='nodes', to='scopes.NodeType'),
        ),
        migrations.AddField(
            model_name='branch',
            name='root',
            field=models.ForeignKey(related_name='branches', to='scopes.Root'),
        ),
        migrations.AlterUniqueTogether(
            name='nodestatetype',
            unique_together=set([('node_type', 'model_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='nodestateargumenttype',
            unique_together=set([('node_type', 'model_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='nodestateargumentprovider',
            unique_together=set([('node_state_argument_provider_type', 'src_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='nodestateargument',
            unique_together=set([('node_state_argument_type', 'src_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='nodestate',
            unique_together=set([('node_state_type', 'src_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='node',
            unique_together=set([('node_type', 'src_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='branch',
            unique_together=set([('root', 'name')]),
        ),
    ]
