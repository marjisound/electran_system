# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_remove_questionsemester_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
