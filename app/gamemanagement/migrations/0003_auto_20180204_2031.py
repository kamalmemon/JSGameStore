# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-04 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamemanagement', '0002_auto_20180125_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='thumbnail_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='savegame',
            name='state',
            field=models.CharField(max_length=500),
        ),
    ]
