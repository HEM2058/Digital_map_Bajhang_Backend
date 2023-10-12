from django.contrib.gis.db import models

class GeoJSONFile(models.Model):
    name = models.CharField(max_length=255)
    geojson_data = models.GeometryCollectionField()
