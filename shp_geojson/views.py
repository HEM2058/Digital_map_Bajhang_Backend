from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import GeoJSONFile
from .serializers import GeoJSONFileSerializer
import zipfile
import io
import fiona
from shapely.geometry import shape

class UploadZipAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        name = request.data.get('name')
        zip_file = request.data.get('zip_file')

        if not name or not zip_file:
            return Response({'error': 'Both name and zip_file are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a GeoJSON file from the uploaded ZIP file
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Assuming there's only one Shapefile in the ZIP, you might need to modify this if there are multiple files.
                shp_file = [f for f in zip_ref.namelist() if f.endswith('.shp')][0]
                with zip_ref.open(shp_file) as shp:
                    with fiona.Collection(shp, 'r') as source:
                        crs = source.crs
                        features = [feature for feature in source]

                geojson_data = {
                    "type": "FeatureCollection",
                    "features": [shape(feat['geometry']).__geo_interface__ for feat in features],
                }

                # Create a GeoJSONFile instance
                geojson_file = GeoJSONFile(name=name, geojson=geojson_data)
                geojson_file.save()

                return Response(GeoJSONFileSerializer(geojson_file).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
