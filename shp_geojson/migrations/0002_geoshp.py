# Generated by Django 3.2.18 on 2023-10-25 09:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shp_geojson', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geoshp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=150)),
                ('file', models.FileField(upload_to='%Y/%m/%d')),
                ('uploaded_date', models.DateField(blank=True, default=datetime.date.today)),
            ],
        ),
    ]
