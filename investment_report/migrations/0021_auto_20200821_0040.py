# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-21 00:40
from __future__ import unicode_literals

import config.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment_report', '0020_auto_20180911_1005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='networkandsupport',
            options={'verbose_name': '11 - Network And Support', 'verbose_name_plural': '11 - Network And Support'},
        ),
        migrations.AlterModelOptions(
            name='rdandinnovationcasestudy',
            options={'verbose_name': '10 - Case Study', 'verbose_name_plural': '10 - Case Study'},
        ),
        migrations.AlterModelOptions(
            name='videocasestudy',
            options={'verbose_name': '10.1 Video case study', 'verbose_name_plural': '10.1 Video case study'},
        ),
        migrations.AlterField(
            model_name='pirrequest',
            name='pdf',
            field=models.FileField(storage=config.s3.PDFS3Boto3Storage(), upload_to=''),
        ),
    ]