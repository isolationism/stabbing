# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-05 03:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('days', '0005_populate_datetime_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lastshooting',
            name='date_event',
        ),
        migrations.RemoveField(
            model_name='laststabbing',
            name='date_event',
        ),
    ]
