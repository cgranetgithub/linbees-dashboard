# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('on_trial', models.BooleanField(default=False, help_text='This field indicate that your are using your workspace for evaluation. Deactivate it once you are ready to go to production mode.', verbose_name='Trial mode')),
                ('contact_name', models.CharField(max_length=255, verbose_name='Main contact name', blank=True)),
                ('contact_email', models.EmailField(help_text='Will be used to send out important message (for instance invoices)', max_length=255, verbose_name='Main contact email', blank=True)),
                ('address1', models.CharField(max_length=255, verbose_name='Address (line1)', blank=True)),
                ('address2', models.CharField(max_length=255, blank=True)),
                ('zipcode', models.IntegerField(null=True, verbose_name='Zipcode', blank=True)),
                ('city', models.CharField(max_length=255, verbose_name='City', blank=True)),
                ('country', models.CharField(max_length=255, verbose_name='Country', blank=True)),
                ('phone_number', models.CharField(max_length=255, verbose_name='Phone number', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active', editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('name', models.SlugField(editable=False, help_text='By default, the dashboard name is your company email domain', unique=True, verbose_name='Dashboard name')),
                ('paid_until', models.DateField(help_text='Date until when the oranization has paid its subscription. At creation time, paid_until is initiaized with now + the default trial period defined in the settings.', verbose_name='Next invoice date', null=True, editable=False)),
                ('monthly_user_fee', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=5, help_text='Monthly rate applied to calculate the monthly fee. Monthly fee is number of active users x rate.', verbose_name='Monthly user fee')),
                ('monthly_fixed_fee', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=7, help_text='Fee per month, independent of the number of users', verbose_name='Monthly fixed fee')),
                ('yearly_fixed_fee', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=8, help_text='Fee per year, independent of the number of users', verbose_name='Yearly fixed fee')),
            ],
        ),
    ]
