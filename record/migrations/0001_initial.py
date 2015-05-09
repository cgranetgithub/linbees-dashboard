# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
        ('workspace', '0001_initial'),
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_agent', models.CharField(max_length=255)),
                ('profile', models.ForeignKey(to='profile.Profile')),
                ('task', models.ForeignKey(to='task.Task')),
                ('workspace', models.ForeignKey(to='workspace.Workspace')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DailyDataPerTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('duration', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('cost', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('children_duration', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('children_cost', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('task', models.ForeignKey(to='task.Task')),
                ('workspace', models.ForeignKey(to='workspace.Workspace')),
            ],
        ),
        migrations.CreateModel(
            name='DailyDataPerTaskPerUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('wage', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('cost', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('duration', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('time_ratio', models.DecimalField(default=0, max_digits=3, decimal_places=2)),
                ('profile', models.ForeignKey(to='profile.Profile')),
                ('task', models.ForeignKey(to='task.Task')),
                ('workspace', models.ForeignKey(to='workspace.Workspace')),
            ],
        ),
        migrations.CreateModel(
            name='ManualRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('start', models.DateTimeField(null=True, blank=True)),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_agent', models.CharField(max_length=255)),
                ('profile', models.ForeignKey(to='profile.Profile')),
                ('task', models.ForeignKey(to='task.Task')),
                ('workspace', models.ForeignKey(to='workspace.Workspace')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='dailydatapertaskperuser',
            unique_together=set([('workspace', 'date', 'task', 'profile')]),
        ),
        migrations.AlterUniqueTogether(
            name='dailydatapertask',
            unique_together=set([('workspace', 'date', 'task')]),
        ),
    ]
