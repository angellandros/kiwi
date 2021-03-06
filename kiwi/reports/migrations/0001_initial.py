# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-14 03:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='date published')),
                ('type', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='datum',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Device'),
        ),
    ]
