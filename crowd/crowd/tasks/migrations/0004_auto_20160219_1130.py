# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-19 16:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20160219_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskassignment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='tasks.Task'),
        ),
        migrations.AlterField(
            model_name='taskassignment',
            name='user_answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.AnswerOption'),
        ),
    ]
