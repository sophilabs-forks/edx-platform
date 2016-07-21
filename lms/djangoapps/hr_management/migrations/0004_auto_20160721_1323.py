# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hr_management', '0003_auto_20160627_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hrmanager',
            name='organization',
            field=models.ForeignKey(to='organizations.Organization'),
        ),
        migrations.AlterField(
            model_name='hrmanager',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
