# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-19 16:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0011_auto_20160419_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskassignment',
            name='user_answer_time',
            field=models.DateTimeField(null=True),
        ),
    ]