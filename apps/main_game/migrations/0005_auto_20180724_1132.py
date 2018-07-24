# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-24 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_game', '0004_auto_20180723_1508'),
    ]

    operations = [
        migrations.RenameField(
            model_name='road',
            old_name='adjacent_fields',
            new_name='adjacent_settlements',
        ),
        migrations.AlterField(
            model_name='road',
            name='player',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='roads', to='login_reg_lobby.Player'),
        ),
    ]