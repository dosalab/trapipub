# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-02 11:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_api', '0003_auto_20170202_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='merchant',
        ),
    ]
