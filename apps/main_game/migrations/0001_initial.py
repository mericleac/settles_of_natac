# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login_reg_lobby', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devcards', to='login_reg_lobby.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource', models.CharField(max_length=45)),
                ('number', models.IntegerField()),
                ('robber', models.BooleanField()),
                ('adjacent_fields', models.ManyToManyField(related_name='_field_adjacent_fields_+', to='main_game.Field')),
            ],
        ),
        migrations.CreateModel(
            name='Road',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Settlement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(default='normal', max_length=45)),
                ('adjacent_fields', models.ManyToManyField(related_name='adjacent_settlements', to='main_game.Field')),
                ('player', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='settlements', to='login_reg_lobby.Player')),
            ],
        ),
        migrations.AddField(
            model_name='road',
            name='adjacent_settlements',
            field=models.ManyToManyField(related_name='adjacent_roads', to='main_game.Settlement'),
        ),
        migrations.AddField(
            model_name='road',
            name='player',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roads', to='login_reg_lobby.Player'),
        ),
    ]
