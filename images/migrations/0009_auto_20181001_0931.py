# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-01 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0008_auto_20181001_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(default=None, upload_to='thumbnails/'),
        ),
    ]
