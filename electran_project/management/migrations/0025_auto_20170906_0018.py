# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-05 23:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0024_auto_20170906_0015'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userquestionsemester',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='userquestionsemester',
            name='question_semester',
        ),
        migrations.RemoveField(
            model_name='userquestionsemester',
            name='user_semester',
        ),
    ]
