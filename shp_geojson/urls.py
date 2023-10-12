from django.urls import path
from .views import UploadZipAPIView   # Import the GeoJSONFileUpload view

urlpatterns = [

    # Add the URL pattern for the GeoJSONFileUpload view
    path('uploadgeojson/', UploadZipAPIView.as_view(), name='upload_geojson'),  # Customize the URL endpoint as needed
]
