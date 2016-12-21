# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_access_group', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomainBlacklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(default=b'', max_length=255)),
            ],
        ),
    ]
