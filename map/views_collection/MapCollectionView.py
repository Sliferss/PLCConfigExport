from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from map.models import PrefabsConveyor
from map.views import is_ajax
from django.utils.crypto import get_random_string
from map.models import PrefabsConveyor, MapSetup, GridParts
import os
from django.conf import settings


class GridView(View):
    template_name = "grid_view.html"
    queryset = None

    def get(self, request, *args, **kwargs):
        context = {}
        if request.GET.get("type") == "filter":
            context = self.populate_prefabs(request, context)
            return JsonResponse(context)
        if request.GET.get("type") == "prefab_get":
            context = self.get_prefab(request, context)
            return JsonResponse(context)
        if not is_ajax(request):
            context = self.initiate_grid(request, context)
            return render(request, self.template_name, context)

    def get_prefab(self, request, context):
        print(request.GET.get("prefab"))
        prefab = PrefabsConveyor.objects.filter(name=request.GET.get("prefab"))
        context["success"] = True
        if not prefab:
            context["success"] = False
            context["error"] = "Prefab no longer in database!"
        context["prefab"] = list(prefab.values())
        return context

    def populate_prefabs(self, request, context):
        prefabs = PrefabsConveyor.objects.all()
        prefab_filter = request.GET.get("prefab_filter")
        if prefab_filter:
            prefabs = prefabs.filter(name__icontains=prefab_filter)
        context["prefab_filter"] = prefab_filter
        context["prefabs"] = list(prefabs.values())
        return context

    def initiate_grid(self, request, context):
        name = request.GET.get("filter_name")
        map_setup = MapSetup.objects.filter(name=name).first()
        context["grid_width"] = map_setup.grid_width
        context["grid_height"] = map_setup.grid_height
        context["filter_name"] = name
        return context


class MapCollectionView(View):
    template_name = "map_collection_view.html"
    queryset = None

    def get(self, request, *args, **kwargs):
        context = {}
        self.queryset = MapSetup.objects.all()
        if not is_ajax(request):
            name = request.GET.get("filter_name")
            if name:
                self.queryset = self.queryset.filter(name__icontains=name)
                context["filter_name"] = name
            context["maps"] = self.queryset
            return render(request, self.template_name, context)
    
    def post(self, request,  *args, **kwargs):
        context = {}
        if request.POST.get("type") == "create":
            context = self.create_map(request, context)
            return JsonResponse(context)
        return JsonResponse(context)

    def create_map(self, request, context):
        name = request.POST.get("name")
        context["error"] = False
        if not name:
            context["error"] = "Missing Name!"
            return context
        if MapSetup.objects.filter(name=name):
            context["error"] = "Name Already Exists!"
            return context
        map_setup_obj = MapSetup.objects.create(name=name)
        map_setup_obj = self.fill_obj_fields(request, map_setup_obj)
        return context

    def fill_obj_fields(self, request, map_setup_obj):
        if request.POST.get("width"):
            map_setup_obj.grid_width = request.POST.get("width")
        if request.POST.get("height"):
            map_setup_obj.grid_height = request.POST.get("height")
        self.image = request.FILES.get('image')
        if self.image:
            map_setup_obj.image = self.upload_image()
        map_setup_obj.save()
        return map_setup_obj

    def upload_image(self):
        image_name = self.image.name
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        if os.path.exists(image_path):
            base, ext = os.path.splitext(image_name)
            unique_id = get_random_string(6)
            image_name = f"{base}_{unique_id}{ext}"
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        with open(image_path, 'wb+') as destination:
            for chunk in self.image.chunks():
                destination.write(chunk)
        return image_path