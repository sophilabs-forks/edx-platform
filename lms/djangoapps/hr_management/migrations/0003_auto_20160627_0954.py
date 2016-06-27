# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import xmodule_django.models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_management', '0002_courseaccessrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCCASettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_id', xmodule_django.models.CourseKeyField(max_length=255, db_index=True)),
                ('require_access_request', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterModelOptions(
            name='courseaccessrequest',
            options={'ordering': ['-created', 'user__email']},
        ),
    ]
