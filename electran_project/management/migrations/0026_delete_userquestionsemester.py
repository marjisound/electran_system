# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-05 23:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0025_auto_20170906_0018'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserQuestionSemester',
        ),
    ]
