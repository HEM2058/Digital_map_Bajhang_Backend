# Generated by Django 3.2.18 on 2023-11-17 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shp_geojson', '0004_alter_reliefrequest_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reliefrequest',
            name='img',
            field=models.FileField(null=True, upload_to='%Y/%m/%d'),
        ),
    ]