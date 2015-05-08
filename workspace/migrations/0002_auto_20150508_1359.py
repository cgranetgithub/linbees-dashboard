# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='paid_until',
            field=models.DateField(default=datetime.date(2015, 8, 6), help_text='Date until when the oranization has paid its subscription. At creation time, paid_until is initiaized with now + the default trial period defined in the settings.', verbose_name='Next invoice date', editable=False),
        ),
    ]
