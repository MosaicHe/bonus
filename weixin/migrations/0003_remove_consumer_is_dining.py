# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 06:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0002_auto_20160414_0603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumer',
            name='is_dining',
        ),
    ]
