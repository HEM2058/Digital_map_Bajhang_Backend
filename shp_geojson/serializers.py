from rest_framework import serializers
from .models import GeoJSONFile
from rest_framework_gis.serializers import GeometrySerializerMethodField

class GeoJSONFileSerializer(serializers.ModelSerializer):
    # Create a custom method field to serialize the geojson field as GeoJSON
    geojson_data = GeometrySerializerMethodField()

    class Meta:
        model = GeoJSONFile
        fields = ('id', 'name', 'geojson', 'created_at', 'updated_at')

    def get_geojson_data(self, obj):
        # Serialize the 'geojson' field as GeoJSON
        return obj.geojson.json
