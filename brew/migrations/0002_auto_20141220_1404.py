# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brew', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottletype',
            name='bottle_size',
            field=models.CharField(max_length=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='measurement',
            name='gravity',
            field=models.CharField(max_length=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='measurement',
            name='temperature',
            field=models.CharField(max_length=3),
            preserve_default=True,
        ),
    ]
