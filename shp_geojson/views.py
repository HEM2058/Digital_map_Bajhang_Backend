import os
import tempfile
import geopandas as gpd
from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import GeoJSONFile
from .serializers import GeoJSONFileSerializer
import zipfile
import io
from shapely.geometry import shape
import fiona

class UploadZipAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        name = request.data.get('name')
        zip_file = request.data.get('zip_file')
        print(f"Received request to upload: {name}")
        print(f"Received zip file: {zip_file}")

        if not name or not zip_file:
            return Response({'error': 'Both name and zip_file are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a temporary directory to extract and process the uploaded files
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Temporary directory created: {temp_dir}")

                # Save the uploaded ZIP file
                zip_file_path = os.path.join(temp_dir, zip_file.name)
                with open(zip_file_path, 'wb') as destination:
                    for chunk in zip_file.chunks():
                        destination.write(chunk)
                print(f"ZIP file saved: {zip_file_path}")

                # Extract the ZIP file
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    # Assuming there's only one Shapefile in the ZIP, you might need to modify this if there are multiple files.
                    shp_file = [f for f in zip_ref.namelist() if f.endswith('.shp')][0]
                    print(f"Selected Shapefile: {shp_file}")
                    with zip_ref.open(shp_file) as shp:
                        with fiona.Collection(shp, 'r') as source:
                            crs = source.crs
                            features = [feature for feature in source]

                    geojson_data = {
                        "type": "FeatureCollection",
                        "features": [shape(feat['geometry']).__geo_interface__ for feat in features],
                    }
                    print("Shapefile successfully converted to GeoJSON.")

                    # Create a GeoJSONFile instance
                    geojson_file = GeoJSONFile(name=name, geojson=geojson_data)
                    geojson_file.save()
                    print("GeoJSON data saved in the database.")

                return Response({'message': 'Data uploaded and converted to GeoJSON successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error during Shapefile processing: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
