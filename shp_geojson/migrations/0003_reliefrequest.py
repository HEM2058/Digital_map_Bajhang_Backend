# Generated by Django 3.2.18 on 2023-11-13 01:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shp_geojson', '0002_auto_20231029_0712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reliefrequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palika', models.CharField(max_length=255)),
                ('ward', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.BigIntegerField()),
                ('citizenship_no', models.CharField(max_length=255)),
                ('House_no', models.CharField(max_length=255)),
                ('disaster', models.CharField(max_length=255)),
                ('img', models.FileField(null=True, upload_to='%Y/%m/%d')),
                ('uploaded_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
            ],
        ),
    ]