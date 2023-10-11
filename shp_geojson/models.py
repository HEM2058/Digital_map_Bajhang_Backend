from django.db import models

# Create your models here.
class GeoJSONFile(models.Model):
    name = models.CharField(max_length=255)
    geojson_data = models.JSONField()