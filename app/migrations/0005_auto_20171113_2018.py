# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-13 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20171113_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='TotalDuration',
            field=models.TextField(blank=True, null=True),
        ),
    ]
