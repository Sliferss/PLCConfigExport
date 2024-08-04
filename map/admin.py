from django.contrib import admin
from .models import PrefabsConveyor, GridParts, MapSetup


@admin.register(PrefabsConveyor)
class PrefabsConveyorAdmin(admin.ModelAdmin):
    list_display = ("name", "image")


@admin.register(GridParts)
class GridPartsAdmin(admin.ModelAdmin):
    list_display = ("name", "map", "position_x", "position_y")


@admin.register(MapSetup)
class MapSetupAdmin(admin.ModelAdmin):
    list_display = ("name", "grid_width", "grid_height", "image")
