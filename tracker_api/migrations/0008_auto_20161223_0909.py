# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-23 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_api', '0007_remove_order_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
