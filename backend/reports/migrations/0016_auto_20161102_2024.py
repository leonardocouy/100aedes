# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-02 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0015_auto_20161102_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='image_url',
            field=models.ImageField(blank=True, upload_to='denuncias/'),
        ),
    ]