from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import GeoJSONFile


class GeoJSONFileAdmin(OSMGeoAdmin):
    list_display = ('name', 'geojson')  # Customize the displayed fields in the admin list view
    search_fields = ('name',)  # Add a search field for the name field

# Register your model with the custom admin class
admin.site.register(GeoJSONFile, GeoJSONFileAdmin)
