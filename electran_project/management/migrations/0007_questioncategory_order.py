# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_question_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='questioncategory',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
