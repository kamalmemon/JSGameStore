# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-14 05:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamemanagement', '0004_auto_20180212_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]