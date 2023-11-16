from django.urls import path
from .views import UploadZipAPIView,GeoJSONFeatureListView,SingleGeoJSONFeatureListView,GeoshpView,ReliefrequestView  # Import the GeoJSONFileUpload view

urlpatterns = [
    # Add the URL pattern for the GeoJSONFileUpload view
    path('uploadgeojson', UploadZipAPIView.as_view(), name='upload_geojson'),  
    path('geojson-features', GeoJSONFeatureListView.as_view(), name='geojson-feature-list'),
    path('geojson-features/<int:pk>', SingleGeoJSONFeatureListView.as_view(), name='single-geojson-feature-list'),
    path('geoshp', GeoshpView.as_view(),name="geoshp"),
    path('relief_request',ReliefrequestView.as_view(),name='relief_request'),
  
    
]
