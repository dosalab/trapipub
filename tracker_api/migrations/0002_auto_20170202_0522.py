# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-02 05:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverylog',
            name='date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
