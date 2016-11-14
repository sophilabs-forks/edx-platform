# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20151208_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkedinaddtoprofileconfiguration',
            name='license_id',
            field=models.TextField(default='', blank=True, help_text='The license number or id for the LinkedIn Add-to-Profile button e.g NASBA 010101'),
            preserve_default=False,
        ),
    ]