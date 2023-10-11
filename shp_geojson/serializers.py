from rest_framework import serializers
from .models import GeoJSONFile

class GeoJSONFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoJSONFile
        fields = ('id', 'name', 'geojson_data', 'created_at', 'updated_at')
