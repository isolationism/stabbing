# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-05 03:18
from __future__ import unicode_literals

from django.db import migrations
from datetime import datetime
from sys import stdout, stderr


def migrate_date_to_datetime(model):
    """Migrates the 'date_event' field to 'datetime_event' for passed object"""
    for modelobject in model.objects.all():
        obj_date = modelobject.date_event
        obj_datetime = datetime(year=obj_date.year, month=obj_date.month,
                                day=obj_date.day, hour=0, minute=0, second=0)
        modelobject.datetime_event = obj_datetime
        modelobject.save()


def migrate_models(apps, schema_editor):
    """Iterates over the types of objects to migrate"""

    # Stabbings
    LastStabbing = apps.get_model('days', 'laststabbing')
    migrate_date_to_datetime(LastStabbing)

    # Shootings
    LastShooting = apps.get_model('days', 'lastshooting')
    migrate_date_to_datetime(LastShooting)


class Migration(migrations.Migration):

    dependencies = [
        ('days', '0004_add_datetime_event'),
    ]

    operations = [
        # REQUIRED or can't resolve model.objects!
        migrations.AlterModelManagers(
            name='laststabbing', managers=[],
        ),
        # REQUIRED or can't resolve model.objects!
        migrations.AlterModelManagers(
            name='lastshooting', managers=[],
        ),
        migrations.RunPython(migrate_models)
    ]
