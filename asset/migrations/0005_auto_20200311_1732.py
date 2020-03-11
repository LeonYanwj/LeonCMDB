# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2020-03-11 09:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0004_auto_20200113_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReqLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_message', models.CharField(choices=[('error', 'error'), ('info', 'info'), ('warning', 'warning')], max_length=16, verbose_name='错误等级')),
                ('message', models.TextField(blank=True, null=True, verbose_name='详细信息')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.Asset')),
            ],
            options={
                'verbose_name_plural': '操作日志',
                'verbose_name': '操作日志',
            },
        ),
        migrations.AlterField(
            model_name='disk',
            name='iface_type',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='接口类型'),
        ),
        migrations.AlterField(
            model_name='ram',
            name='capacity',
            field=models.IntegerField(verbose_name='内存大小（MB）'),
        ),
        migrations.AlterField(
            model_name='ram',
            name='slot',
            field=models.CharField(max_length=64, verbose_name='插槽'),
        ),
    ]
