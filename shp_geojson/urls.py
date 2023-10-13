from django.urls import path
from .views import UploadZipAPIView,GeoJSONFeatureListView  # Import the GeoJSONFileUpload view

urlpatterns = [
    # Add the URL pattern for the GeoJSONFileUpload view
    path('uploadgeojson/', UploadZipAPIView.as_view(), name='upload_geojson'),  
    path('geojson-features/', GeoJSONFeatureListView.as_view(), name='geojson-feature-list'),
]
