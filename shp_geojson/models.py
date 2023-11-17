# Import necessary modules
from django.db import models
import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import geopandas as gpd
import os
import zipfile
import glob
from geoalchemy2 import Geometry, WKTElement
from geo.Geoserver import Geoserver
from sqlalchemy import create_engine, text  # Import the text function
# Set the GeoServer URL
GEOSERVER_URL = 'http://localhost:8080/geoserver'

# Define your Django models
class GeoJSONfeature(models.Model):
    name = models.CharField(max_length=255)
    geojson = models.JSONField()

class Reliefrequest(models.Model):
    #location information
    palika = models.CharField(max_length=255)
    ward = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    #client information
    name = models.CharField(max_length=255)
    phone = models.BigIntegerField()
    citizenship_no = models.CharField(max_length=255)
    House_no = models.CharField(max_length=255)
    disaster = models.CharField(max_length=255)
    img = models.FileField(upload_to='%Y/%m/%d', null=True)
    uploaded_date = models.DateField(default=datetime.date.today, blank=True, null=True)

class Place(models.Model):
    palika = models.CharField(max_length=255, blank=True)
    place_title = models.CharField(max_length=255)
    place_description = models.TextField(max_length=120)
    place_image = models.FileField(upload_to='places/', null=True)
    place_coordinates = models.CharField(max_length=255)

    def __str__(self):
        return self.place_title
# Define the 'localLevels' list with the available choices
localLevels = [
    'Bithadchir',
    'Bungal',
    'Chabispathivera',
    'Durgathali',
    'JayaPrithivi',
    'Kedarseu',
    'Khaptadchhanna',
    'Masta',
    'Saipal',
    'Surma',
    'Talkot',
    'Thalara',
]

class Geoshp(models.Model):
    Palika = models.CharField(max_length=50, choices=[('', 'Select Palika')] + [(level, level) for level in localLevels], null=True)
    store = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    file = models.FileField(upload_to='%Y/%m/%d', null=True)
    uploaded_date = models.DateField(default=datetime.date.today, blank=True, null=True)
    
    def __str__(self):
        return self.name

# Connect to the PostgreSQL database
conn_str = 'postgresql://postgres:mappers123@localhost:5432/map'
engine = create_engine(conn_str)

# Define a function to import a shapefile into the PostgreSQL database
def import_shapefile(shapefile_path, name):
    gdf = gpd.read_file(shapefile_path)
    gdf.to_postgis(con=engine, schema='public', name=name, if_exists="replace")
    print(f'Shapefile "{name}" imported into PostgreSQL.')

# Define a function to publish a shapefile to GeoServer with a specific workspace and store name
def publish_shapefile(name, workspace_name, store_name):
    geo = Geoserver(GEOSERVER_URL, username='admin', password='geoserver')
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f'name="{name}",workspace="{workspace_name}",store="{store_name}".')
    # Creating a feature store in GeoServer
    geo.create_featurestore(store_name=store_name, workspace=workspace_name, db='map', host='localhost', pg_user='mappers',
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
        if instance.Palika and instance.store:
            print(f"Imported and published shapefile '{instance.name}' with Palika='{instance.Palika}' and store='{instance.store}'")
            publish_shapefile(instance.name, workspace_name=instance.Palika, store_name=instance.store)

# Define a signal handler to delete data when a Geoshp instance is deleted
@receiver(models.signals.post_delete, sender=Geoshp)
def delete_data(sender, instance, **kwargs):
    # Delete the table from the PostgreSQL database
    conn = engine.connect()  # Obtain a connection from the engine
    delete_sql = text(f'DROP TABLE IF EXISTS "public"."{instance.name}"')
    conn.execute(delete_sql)  # Execute the SQL command
    conn.close()  # Close the connection

    # Connect to GeoServer and delete the layer
    geo = Geoserver(GEOSERVER_URL, username='admin', password='geoserver')
    geo.delete_layer(instance.name)
