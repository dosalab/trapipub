# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-14 07:00
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('point', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('slug', models.SlugField(default='slug', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('address', models.CharField(max_length=150)),
                ('point', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('slug', models.SlugField(default='slug', primary_key=True, serialize=False)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(default='slug')),
                ('carrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Carrier')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.date.today)),
                ('details', models.CharField(max_length=50)),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Delivery')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=150)),
                ('point', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('payment_info', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('date', models.DateTimeField(default=datetime.date.today)),
                ('notes', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice_number', models.CharField(max_length=20, unique=True)),
                ('from_address', models.CharField(max_length=150)),
                ('from_point', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('to_address', models.CharField(max_length=150)),
                ('to_point', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('slug', models.SlugField(default='slug', primary_key=True, serialize=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Customer')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Merchant')),
            ],
        ),
        migrations.CreateModel(
            name='TrackerSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('sites', models.ManyToManyField(to='sites.Site')),
            ],
        ),
        migrations.AddField(
            model_name='delivery',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Order'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.DeliveryStatus'),
        ),
        migrations.AddField(
            model_name='carrier',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_api.Merchant'),
        ),
        migrations.AddField(
            model_name='carrier',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
