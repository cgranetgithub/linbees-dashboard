# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '__first__'),
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailySalary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(verbose_name='End date')),
                ('daily_wage', models.DecimalField(default=0, help_text='This represents the cost of the employee per day', verbose_name='Daily wage', max_digits=8, decimal_places=2)),
                ('profile', models.ForeignKey(verbose_name='User', to='profile.Profile')),
                ('workspace', models.ForeignKey(to='workspace.Workspace')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
