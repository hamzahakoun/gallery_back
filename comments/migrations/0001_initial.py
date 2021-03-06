# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-26 11:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('content', models.TextField(max_length=1000)),
                ('is_parent', models.BooleanField()),
                ('object_id', models.PositiveIntegerField(default=1)),
                ('content_type', models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
    ]
