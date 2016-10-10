# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20151208_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='job_role',
            field=models.CharField(blank=True, max_length=32, null=True, choices=[(b'SharePoint Administrator', b'SharePoint Administrator'), (b'SharePoint Architect', b'SharePoint Architect'), (b'SharePoint Developer', b'SharePoint Developer'), (b'SharePoint Consultant', b'SharePoint Consultant'), (b'IT Management', b'IT Management'), (b'Other', b'Other')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='telephone_number',
            field=models.CharField(max_length=15, blank=True),
        ),
    ]
