from django.contrib import admin
from .models import GeoJSONfeature, Geoshp, Reliefrequest
from django.contrib.gis.admin import OSMGeoAdmin



# Register your model with the custom admin class
admin.site.register(GeoJSONfeature)
admin.site.register(Reliefrequest)
@admin.register(Geoshp)
class GeoshpAdmin(OSMGeoAdmin):
    pass