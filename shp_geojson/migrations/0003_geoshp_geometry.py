# Generated by Django 3.2.18 on 2023-10-25 11:04

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shp_geojson', '0002_geoshp'),
    ]

    operations = [
        migrations.AddField(
            model_name='geoshp',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326),
        ),
    ]
