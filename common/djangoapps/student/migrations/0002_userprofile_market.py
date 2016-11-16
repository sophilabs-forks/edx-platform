# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='market',
            field=models.IntegerField(blank=True, null=True, choices=[(b'23', b'Atlanta'), (b'60', b'Austin'), (b'46', b'Baltimore'), (b'102', b'Boise'), (b'10', b'Boston'), (b'61', b'Charlotte'), (b'14', b'Chicago'), (b'34', b'Connecticut'), (b'22', b'Dallas'), (b'27', b'Denver'), (b'24', b'Detroit'), (b'826', b'Houston'), (b'58', b'Indianapolis'), (b'13', b'Los Angeles'), (b'33', b'Miami'), (b'20', b'Minneapolis'), (b'807', b'Moline'), (b'30', b'New Jersey'), (b'11', b'New York City'), (b'51', b'Northern Virginia'), (b'32', b'Ohio'), (b'19', b'Orange County'), (b'72', b'Orlando'), (b'18', b'Philadelphia'), (b'31', b'Phoenix'), (b'41', b'Portland, OR'), (b'803', b'Raleigh/Durham'), (b'73', b'Rhode Island'), (b'78', b'Richmond'), (b'16', b'San Diego'), (b'12', b'San Francisco'), (b'17', b'Seattle'), (b'15', b'Silicon Valley'), (b'37', b'St. Louis'), (b'68', b'Tampa'), (b'25', b'Washington, DC'), (b'881', b'Wisconsin'), (b'XX', b'Canada'), (b'40', b'Toronto'), (b'47', b'Vancouver'), (b'XX', b'Europe'), (b'43', b'Amsterdam'), (b'29', b'London'), (b'35', b'Paris'), (b'XX', b'Australia'), (b'36', b'Melbourne'), (b'39', b'Sydney'), (b'XX', b'Japan'), (b'92', b'Fukuoka'), (b'79', b'Nagoya'), (b'64', b'Osaka'), (b'44', b'Tokyo')]),
        ),
    ]
