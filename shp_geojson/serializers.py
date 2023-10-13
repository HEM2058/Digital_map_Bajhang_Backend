from rest_framework import serializers
from .models import GeoJSONfeature
class ShapefileUploadSerializer(serializers.Serializer):
    zip_file = serializers.FileField()

class ConvertedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoJSONfeature
        fields = ("name",'geojson')
