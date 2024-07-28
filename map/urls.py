from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from map.views import Index
from map.views_collection.PrefabsView import PrefabsView
from map.views_collection.MapCollectionView import MapCollectionView

app_name = "map"

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("prefabs/", PrefabsView.as_view(), name="prefabs_view"),
    path("map_collection/", MapCollectionView.as_view(), name="map_collection"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
