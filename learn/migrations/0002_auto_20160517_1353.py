# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 11:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='languagedictionnary',
            old_name='name',
            new_name='language',
        ),
    ]
