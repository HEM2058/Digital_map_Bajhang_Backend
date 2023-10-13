from django.db import models


class GeoJSONfeature(models.Model):
    name = models.CharField(max_length=255)
    geojson = models.JSONField()  

   