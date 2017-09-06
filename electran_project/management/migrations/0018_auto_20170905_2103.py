# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-05 20:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0017_auto_20170902_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquestionsemester',
            name='question_semester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.QuestionSemester'),
        ),
        migrations.AlterField(
            model_name='userquestionsemester',
            name='user_semester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.UserSemester'),
        ),
    ]
