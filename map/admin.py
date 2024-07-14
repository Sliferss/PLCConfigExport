from django.contrib import admin
from .models import PrefabsConveyor, GridParts, MapSetup

@admin.register(PrefabsConveyor)
class PrefabsConveyorAdmin(admin.ModelAdmin):
    list_display = ('name', 'length', 'width', 'height', 'speed')

@admin.register(GridParts)
class GridPartsAdmin(admin.ModelAdmin):
    list_display = ('name', 'map', 'length', 'width', 'height', 'speed')

@admin.register(MapSetup)
class MapSetupAdmin(admin.ModelAdmin):
    list_display = ('name', 'grid_width', 'grid_height')
