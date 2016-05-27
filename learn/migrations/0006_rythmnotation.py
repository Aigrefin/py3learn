# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-25 17:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learn', '0005_missed_field_size_and_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='RythmNotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('successes', models.BigIntegerField()),
                ('next_repetition', models.DateField()),
                ('translation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learn.Translation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]