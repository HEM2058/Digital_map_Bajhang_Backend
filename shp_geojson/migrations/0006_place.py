# Generated by Django 3.2.18 on 2023-11-17 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shp_geojson', '0005_alter_reliefrequest_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palika', models.CharField(blank=True, max_length=255)),
                ('place_title', models.CharField(max_length=255)),
                ('place_description', models.TextField(max_length=120)),
                ('place_image', models.FileField(null=True, upload_to='places/')),
                ('place_coordinates', models.CharField(max_length=255)),
            ],
        ),
    ]
