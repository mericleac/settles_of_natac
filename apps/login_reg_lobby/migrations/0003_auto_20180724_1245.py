# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-24 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg_lobby', '0002_auto_20180724_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('password_confirmation', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='player',
            name='brick',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='lumber',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='ore',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='sheep',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='vic_points',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='wheat',
            field=models.IntegerField(),
        ),
    ]
