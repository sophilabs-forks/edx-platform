# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_management', '0005_hrmanager_send_monthly_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitewideReportList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('send_monthly_report', models.BooleanField(default=False)),
            ],
        ),
    ]
