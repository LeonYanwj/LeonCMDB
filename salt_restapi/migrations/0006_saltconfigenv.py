# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2020-04-24 10:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salt_restapi', '0005_auto_20200423_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaltConfigEnv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('webserver', models.GenericIPAddressField()),
                ('timeout', models.IntegerField()),
                ('salt_master', models.GenericIPAddressField()),
            ],
        ),
    ]