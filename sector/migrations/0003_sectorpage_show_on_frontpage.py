# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-21 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sector', '0002_industrieslandingpage_hero_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sectorpage',
            name='show_on_frontpage',
            field=models.BooleanField(default=False),
        ),
    ]
