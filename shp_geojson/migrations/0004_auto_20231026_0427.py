# Generated by Django 3.2.18 on 2023-10-26 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shp_geojson', '0003_geoshp_geometry'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleGeoJSONfeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geojson', models.JSONField()),
            ],
        ),
        migrations.RemoveField(
            model_name='geoshp',
            name='geometry',
        ),
    ]
