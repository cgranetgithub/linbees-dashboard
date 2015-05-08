# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0001_initial'),
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255, editable=False)),
                ('value', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('profile', models.ForeignKey(editable=False, to='profile.Profile')),
                ('workspace', models.ForeignKey(to='workspace.Workspace')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='preference',
            unique_together=set([('workspace', 'profile', 'key')]),
        ),
    ]
