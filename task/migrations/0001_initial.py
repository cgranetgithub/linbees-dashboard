# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0001_initial'),
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('monitored', models.BooleanField(default=True, verbose_name='Monitored')),
                ('primary', models.BooleanField(default=False, verbose_name='Primary')),
                ('personal', models.BooleanField(default=False, verbose_name='Personal')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.CharField(max_length=255, verbose_name='Description', blank=True)),
                ('start_date', models.DateField(null=True, verbose_name='Start date (planned)', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='End date (planned)', blank=True)),
                ('additional_cost', models.IntegerField(null=True, verbose_name='Additional cost', blank=True)),
                ('cost_estimate', models.IntegerField(null=True, verbose_name='Cost (planned)', blank=True)),
                ('time_estimate', models.IntegerField(null=True, verbose_name='Time (planned, in hours)', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('owner', models.ForeignKey(verbose_name='Owned by', to='profile.Profile')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
        ),
        migrations.CreateModel(
            name='TaskGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('description', models.CharField(max_length=255, verbose_name='Description', blank=True)),
                ('workspace', models.ForeignKey(to='workspace.Workspace')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('description', models.CharField(max_length=255, verbose_name='Description', blank=True)),
                ('workspace', models.ForeignKey(to='workspace.Workspace')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='task',
            name='p_group',
            field=models.ForeignKey(verbose_name='Group', blank=True, to='task.TaskGroup', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='p_type',
            field=models.ForeignKey(verbose_name='Type', blank=True, to='task.TaskType', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children_task', blank=True, to='task.Task', help_text='Parent project', null=True, verbose_name='Parent project'),
        ),
        migrations.AddField(
            model_name='task',
            name='workspace',
            field=models.ForeignKey(to='workspace.Workspace'),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('workspace', 'name', 'parent')]),
        ),
    ]
