from rest_framework import serializers
from .models import GeoJSONfeature,Geoshp,Reliefrequest

class ShapefileUploadSerializer(serializers.Serializer):
    zip_file = serializers.FileField()

class ConvertedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoJSONfeature
        fields = ("name",'geojson')

class Geoshpserializer(serializers.ModelSerializer):
      class Meta:
        model = Geoshp
        fields = ("id","Palika","name")

class ReliefrequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reliefrequest
        fields = ('__all__')