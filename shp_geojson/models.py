# Import necessary modules
from django.db import models
import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import geopandas as gpd
import os
import zipfile
import glob
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement
from geo.Geoserver import Geoserver

# Set the GeoServer URL
GEOSERVER_URL = 'http://localhost:8080/geoserver'

# Define your Django models
class GeoJSONfeature(models.Model):
    name = models.CharField(max_length=255)
    geojson = models.JSONField()

class Geoshp(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True)
    file = models.FileField(upload_to='%Y/%m/%d')
    uploaded_date = models.DateField(default=datetime.date.today, blank=True)

    def __str__(self):
        return self.name

# Connect to the PostgreSQL database
conn_str = 'postgresql://postgres:mappers123@localhost:5432/gis'
engine = create_engine(conn_str)

# Define a function to import a shapefile into the PostgreSQL database
def import_shapefile(shapefile_path, name):
    gdf = gpd.read_file(shapefile_path)
    gdf.to_postgis(con=engine, schema='public', name=name, if_exists="replace")
    print(f'Shapefile "{name}" imported into PostgreSQL.')

# Define a function to publish a shapefile to GeoServer with a specific workspace and store name
def publish_shapefile(name, workspace_name, store_name):
    geo = Geoserver(GEOSERVER_URL, username='admin', password='geoserver')

    # Creating a feature store in GeoServer
    geo.create_featurestore(store_name=store_name, workspace=workspace_name, db='postgres', host='localhost', pg_user='postgres',
                         pg_password='mappers123', schema='public')
    print(f'Feature store "{store_name}" created in workspace "{workspace_name}".')

    # Publishing the shapefile to the feature store
    geo.publish_featurestore(workspace=workspace_name, store_name=store_name, pg_table=name)
    print(f'Shapefile "{name}" published to GeoServer feature store "{store_name}" in workspace "{workspace_name}".')

    # # Creating an outline feature style
    # geo.create_outline_featurestyle(store_name, workspace=workspace_name)
    # print(f'Outline feature style created for feature store "{store_name}" in workspace "{workspace_name}".')

    # # Publishing the style
    # geo.publish_style(layer_name=name, style_name=store_name, workspace=workspace_name)
    # print(f'Style "{store_name}" published for shapefile "{name}" in workspace "{workspace_name}".')

# Define a signal handler to import and publish a shapefile when a new Shapefile object is created
@receiver(models.signals.post_save, sender=Geoshp)
def import_and_publish_shapefile(sender, instance, created, **kwargs):
    if created:
        import_shapefile(instance.file.path, instance.name)
        publish_shapefile(instance.name, workspace_name='digitalmap', store_name='digitalmap123')
