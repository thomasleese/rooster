# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-31 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0004_auto_20160213_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobresource',
            name='per_volunteer',
            field=models.BooleanField(default=True),
        ),
    ]