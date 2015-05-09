# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preference', '0001_initial'),
        ('workspace', '0001_initial'),
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference',
            name='profile',
            field=models.ForeignKey(editable=False, to='profile.Profile'),
        ),
        migrations.AddField(
            model_name='preference',
            name='workspace',
            field=models.ForeignKey(to='workspace.Workspace'),
        ),
        migrations.AlterUniqueTogether(
            name='preference',
            unique_together=set([('workspace', 'profile', 'key')]),
        ),
    ]
