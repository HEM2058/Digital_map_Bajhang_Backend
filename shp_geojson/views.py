from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ShapefileUploadSerializer, ConvertedDataSerializer
import tempfile
import os
import zipfile
import shapefile
import json
from .models import GeoJSONfeature # Import the GeoJSONFile model

class UploadZipAPIView(APIView):
    def post(self, request):
        print("Inside function")
        name = request.data.get('name')  # Assuming 'name' is a key in the POST request data
        zip_file = request.data.get('zip_file')  # Assuming 'zip_file' is a key in the POST request data
        print(f"Received name: {name}")
        print(f"Received zip_file: {zip_file}")

        if zip_file is None:
            print("zip_file is missing in the POST request.")
            return Response({'error': 'zip_file is required in the POST request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ShapefileUploadSerializer(data={'name': name, 'zip_file': zip_file})
        
        if serializer.is_valid():
            zip_file = serializer.validated_data['zip_file']

            # Create a temporary directory to extract the contents of the zip file
            temp_dir = tempfile.TemporaryDirectory()
            print(f"Created temporary directory: {temp_dir.name}")

            try:
                # Extract the contents of the zip file to the temporary directory
                with zipfile.ZipFile(zip_file, 'r') as z:
                    z.extractall(temp_dir.name)
                print(f"Extracted files to: {temp_dir.name}")

                # Find the .shp file in the extracted contents
                shapefile_path = None
                for root, dirs, files in os.walk(temp_dir.name):
                    for file in files:
                        if file.endswith(".shp"):
                            shapefile_path = os.path.join(root, file)
                            break
                    if shapefile_path:
                        break

                if shapefile_path:
                    print(f"Shapefile found: {shapefile_path}")
                    # Read Shapefile and convert to GeoJSON
                    shape_reader = shapefile.Reader(shapefile_path)
                    fields = shape_reader.fields[1:]
                    field_names = [field[0] for field in fields]
                    features = []
                    for shape_record in shape_reader.shapeRecords():
                        geometry = shape_record.shape.__geo_interface__
                        attributes = dict(zip(field_names, shape_record.record))
                        features.append({
                            'type': 'Feature',
                            'geometry': geometry,
                            'properties': attributes
                        })
                    geojson_data = {
                        'type': 'FeatureCollection',
                        'features': features
                    }

                    # Save the converted GeoJSON data to the GeoJSONFile model
                    geojson_file = GeoJSONfeature(name=name, geojson=geojson_data)
                    geojson_file.save()

                    # Return the converted GeoJSON data
                    return Response(geojson_data, status=status.HTTP_200_OK)
                 
                else:
                    print("Shapefile not found in the uploaded ZIP file.")
                    return Response({'error': 'Shapefile not found in the uploaded ZIP file.'}, status=status.HTTP_400_BAD_REQUEST)

            finally:
                # Clean up extracted files and temporary directory
                temp_dir.cleanup()
                print("Temporary directory and extracted files cleaned up.")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class GeoJSONFeatureListView(APIView):
    def get(self, request):
        geojson_features = GeoJSONFeature.objects.all()
        serializer = ConvertedDataSerializer(geojson_features, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)