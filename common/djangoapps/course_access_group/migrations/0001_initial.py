# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import xmodule_django.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseAccessGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='CourseStub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255)),
                ('course_id', xmodule_django.models.CourseKeyField(default=b'', unique=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='courseaccessgroup',
            name='courses',
            field=models.ManyToManyField(to='course_access_group.CourseStub', blank=True),
        ),
        migrations.AddField(
            model_name='courseaccessgroup',
            name='students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
