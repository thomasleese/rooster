# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-02 21:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0005_auto_20160302_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2016, 3, 2, 21, 13, 17, 879760)),
        ),
    ]
