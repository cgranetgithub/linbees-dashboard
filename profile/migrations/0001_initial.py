# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('workspace', '__first__'),
        ('department', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('title', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('has_accepted_terms', models.BooleanField(default=False, verbose_name='Accepted terms')),
                ('has_dashboard_access', models.BooleanField(default=False, help_text='Designates whether the user can access the dashboard.', verbose_name='Dashboard access')),
                ('is_hr', models.BooleanField(default=False, help_text='Designates whether the user has the HR permissions.', verbose_name='HR status')),
                ('is_primary', models.BooleanField(default=False, help_text='Designates whether the user has the permissions to administrate primary tasks/projects.', verbose_name='Primary status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('department', models.ForeignKey(blank=True, to='department.Department', null=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', verbose_name='Manager', blank=True, to='profile.Profile', null=True)),
                ('power_transfer', models.ManyToManyField(related_name='power_transfer_rel_+', verbose_name='has power transfer from', to='profile.Profile', blank=True)),
                ('workspace', models.ForeignKey(to='workspace.Workspace')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
