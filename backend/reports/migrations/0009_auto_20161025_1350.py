# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-25 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0008_auto_20161025_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reason',
            field=models.TextField(null=True, verbose_name='Razão do Status'),
        ),
    ]