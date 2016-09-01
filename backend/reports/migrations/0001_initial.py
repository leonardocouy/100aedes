# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-01 10:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='Endereço')),
                ('district', models.CharField(max_length=100, verbose_name='Bairro')),
                ('number', models.IntegerField(verbose_name='Número')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('status', models.IntegerField(choices=[(0, 'Não Enviada'), (1, 'Enviada'), (2, 'Em análise'), (3, 'Foco tratado'), (4, 'Foco não encontrado')], default=0, verbose_name='Status')),
                ('reason', models.CharField(max_length=155, null=True, verbose_name='Razão do Status')),
                ('image_url', models.ImageField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='core.City')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Denúncias',
                'verbose_name': 'Denúncia',
            },
        ),
    ]
