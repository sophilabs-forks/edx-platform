# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_management', '0004_auto_20160721_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='hrmanager',
            name='send_monthly_report',
            field=models.BooleanField(default=False),
        ),
    ]
