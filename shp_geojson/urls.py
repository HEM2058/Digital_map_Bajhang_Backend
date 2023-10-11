from django.urls import path
from .views import GeoJSONFileUpload  # Import the GeoJSONFileUpload view

urlpatterns = [
    

    # Add the URL pattern for the GeoJSONFileUpload view
    path('uploadgeojson/', GeoJSONFileUpload.as_view(), name='upload_geojson'),  # Customize the URL endpoint as needed
]
