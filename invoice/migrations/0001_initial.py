# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('sent_at', models.DateTimeField(null=True, verbose_name='sent at', blank=True)),
                ('month', models.IntegerField(verbose_name='month')),
                ('year', models.IntegerField(verbose_name='year')),
                ('amount', models.IntegerField(verbose_name='amount')),
                ('comment', models.CharField(max_length=255, verbose_name='comment', blank=True)),
                ('pdf', models.FileField(upload_to=b'invoices')),
                ('workspace', models.ForeignKey(to='workspace.Workspace')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
