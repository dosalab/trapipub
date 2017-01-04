# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-02 11:45
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.IntegerField()),
                ('location', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=30)),
                ('phone', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carriers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Carrier')),
            ],
        ),
        migrations.CreateModel(
            name='Deliverystage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.date.today)),
                ('info', models.CharField(max_length=50)),
                ('terminal', models.BooleanField()),
                ('location', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('paymentinfo', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.date.today)),
                ('notes', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoicenumber', models.CharField(max_length=20)),
                ('deliveryaddress', models.CharField(max_length=200)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Customer')),
                ('merchants', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Merchant')),
            ],
        ),
        migrations.CreateModel(
            name='Orderstatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('date', models.DateTimeField(default=datetime.date.today)),
                ('info', models.CharField(max_length=50)),
                ('terminal', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('date', models.DateTimeField(default=datetime.date.today)),
                ('deliverys', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Delivery')),
                ('orders', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='packages',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Package'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Orderstatus'),
        ),
        migrations.AddField(
            model_name='deliverystage',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Order'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='packages',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Package'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Deliverystage'),
        ),
        migrations.AddField(
            model_name='carrier',
            name='deliverise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Delivery'),
        ),
        migrations.AddField(
            model_name='carrier',
            name='merchants',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Merchant'),
        ),
    ]