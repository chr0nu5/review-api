# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-20 04:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0002_auto_20161120_0401'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]