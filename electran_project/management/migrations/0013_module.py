# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0012_auto_20170821_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_code', models.CharField(max_length=50)),
                ('module_name', models.CharField(max_length=200)),
            ],
        ),
    ]
