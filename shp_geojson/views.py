import os
import tempfile
import zipfile
import geopandas as gpd
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from .models import GeoJSONFile  # Import your GeoJSON model
from .serializers import GeoJSONFileSerializer

class GeoJSONFileUpload(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        # Get the uploaded ZIP file and layer name
        layer_name = request.data.get('layerName')
        shp_zip_file = request.FILES.get('shpFile')

        if not shp_zip_file:
            return JsonResponse({'error': 'Please provide a valid ZIP file.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a temporary directory to extract the files
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract the ZIP file to the temporary directory
                with zipfile.ZipFile(shp_zip_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Find the SHP file within the extracted files
                shp_files = [f for f in os.listdir(temp_dir) if f.lower().endswith('.shp')]

                if not shp_files:
                    return JsonResponse({'error': 'No SHP file found in the ZIP archive.'}, status=status.HTTP_400_BAD_REQUEST)

                # Assume the first SHP file found is the main one (you may adjust this logic as needed)
                shp_file_path = os.path.join(temp_dir, shp_files[0])

                # Read the SHP file using geopandas
                gdf = gpd.read_file(shp_file_path)

                # Convert to GeoJSON format
                geojson_data = gdf.to_json()

                # Save the GeoJSON data to your model (assuming you have a model named GeoJSONFile)
                geojson_instance = GeoJSONFile(name=layer_name, geojson_data=geojson_data)
                geojson_instance.save()

                # Serialize the model instance for response
                serializer = GeoJSONFileSerializer(geojson_instance)

                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
