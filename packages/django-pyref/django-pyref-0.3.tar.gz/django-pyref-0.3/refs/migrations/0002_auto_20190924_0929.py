# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-09-24 09:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ref',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='ref',
            name='note_html',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='ref',
            name='note_latex',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='ref',
            name='authors',
            field=models.TextField(blank=True, help_text='Comma-delimited names with space-separated initials first (no ANDs). e.g. "A. N. Other, B.-C. Person Jr., Ch. Someone-Someone, N. M. L. Haw Haw"'),
        ),
    ]
