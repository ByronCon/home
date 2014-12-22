# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch_text', models.CharField(max_length=200)),
                ('brew_date', models.DateTimeField(verbose_name=b'date brewed')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BottleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bottle_type_text', models.CharField(max_length=200)),
                ('bottle_size', models.CharField(max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bottling',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_bottled', models.DateTimeField(verbose_name=b'date bottled')),
                ('num_bottles', models.IntegerField(default=0)),
                ('markings', models.CharField(max_length=10)),
                ('notes', models.CharField(max_length=200)),
                ('batch', models.ForeignKey(to='brew.Batch')),
                ('bottle_type', models.ForeignKey(to='brew.BottleType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GravityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gravity_type_text', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('measurement_date', models.DateTimeField(verbose_name=b'date measured')),
                ('gravity', models.CharField(max_length=2)),
                ('temperature', models.CharField(max_length=2)),
                ('batch', models.ForeignKey(to='brew.Batch')),
                ('gravity_type', models.ForeignKey(to='brew.GravityType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipe_text', models.CharField(max_length=200)),
                ('recipe_ingredients', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bottling',
            name='measurement',
            field=models.ForeignKey(to='brew.Measurement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='batch',
            name='recipe',
            field=models.ForeignKey(to='brew.Recipe'),
            preserve_default=True,
        ),
    ]
