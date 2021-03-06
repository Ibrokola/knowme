# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-08 00:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='slug',
            field=models.SlugField(default='abc-123'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='slug',
            field=models.SlugField(default='abc-123'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='slug',
            field=models.SlugField(default='abc-123'),
            preserve_default=False,
        ),
    ]
