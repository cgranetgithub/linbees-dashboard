# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='has_dashboard_access',
            field=models.BooleanField(default=False, help_text='Authorize the user to access the dashboard. The user will only see his own projects, the members of his teams and their projects.', verbose_name='Dashboard access'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_hr',
            field=models.BooleanField(default=False, help_text='Authorize the user to see and modify users information (name, tile, salary, activity). But only for the members of his teams.', verbose_name='Users information access'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_primary',
            field=models.BooleanField(default=False, help_text='Authorize the user to see and modify all projects and create root (primary) projects.', verbose_name='Projects full access'),
        ),
    ]
