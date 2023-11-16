from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ShapefileUploadSerializer, ConvertedDataSerializer, GeoshpSerializer, ReliefrequestSerializer
import tempfile
import os
import zipfile
import shapefile
import json
from .models import GeoJSONfeature,Geoshp,Reliefrequest  # Import the GeoJSONFile model
from rest_framework import generics
from pyproj import Transformer, CRS
from rest_framework.permissions import IsAuthenticated
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

                    # Read the CRS information from the .prj file
                    prj_file_path = os.path.splitext(shapefile_path)[0] + ".prj"
                    if os.path.isfile(prj_file_path):
                        with open(prj_file_path, 'r') as prj_file:
                            prj_text = prj_file.read()
                            source_crs = CRS(prj_text)

                        # Use the pyproj library to create a transformer for coordinate transformation
                        transformer = Transformer.from_crs(source_crs, 'EPSG:4326', always_xy=True)

                        fields = shape_reader.fields[1:]
                        field_names = [field[0] for field in fields]
                        features = []
                        for shape_record in shape_reader.shapeRecords():
                            # Transform the geometry to EPSG:4326 (WGS84)
                            geometry = shape_record.shape.__geo_interface__
                            attributes = dict(zip(field_names, shape_record.record))

                            # Check if the geometry coordinates are not empty
                            if geometry['coordinates']:
                                # Transform each coordinate in the geometry separately
                                for i, coord in enumerate(geometry['coordinates']):
                                    if len(coord) == 2:  # Ensure the coordinate has both lon and lat
                                        lon, lat = transformer.transform(coord[0], coord[1])
                                        geometry['coordinates'][i] = [lon, lat]

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
                        print("Warning: .prj file is missing. Proceeding without specifying the source CRS.")
                        return Response({'error': '.prj file is missing. Cannot determine source CRS.'}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    print("Shapefile not found in the uploaded ZIP file.")
                    return Response({'error': 'Shapefile not found in the uploaded ZIP file.'}, status=status.HTTP_400_BAD_REQUEST)

            finally:
                # Clean up extracted files and the temporary directory
                temp_dir.cleanup()
                print("Temporary directory and extracted files cleaned up.")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GeoJSONFeatureListView(generics.ListAPIView):
    queryset = GeoJSONfeature.objects.all()
    serializer_class = ConvertedDataSerializer

class SingleGeoJSONFeatureListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GeoJSONfeature.objects.all()
    serializer_class = ConvertedDataSerializer

class GeoshpView(generics.ListCreateAPIView):
    queryset = Geoshp.objects.all()
    serializer_class = GeoshpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

class ReliefrequestView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Reliefrequest.objects.all()
    serializer_class = ReliefrequestSerializer

class SingleReliefrequestView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReliefrequestSerializer
    lookup_field = 'palika'  # Set the lookup field to match your URL parameter

    def get_queryset(self):
        # Retrieve the Palika parameter from the URL
        palika = self.kwargs['palika']
        
        # Filter ReliefRequest objects based on Palika
        queryset = Reliefrequest.objects.filter(palika=palika)

        return queryset