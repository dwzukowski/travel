# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='description',
            field=models.CharField(default='A nice place', max_length=255),
            preserve_default=False,
        ),
    ]
