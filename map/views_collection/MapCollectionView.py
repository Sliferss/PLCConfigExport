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
        type = request.GET.get("type")
        if type == "filter":
            context = self.populate_prefabs(request, context)
            return JsonResponse(context)
        if type == "prefab_get":
            context = self.get_prefab(request, context)
            return JsonResponse(context)
        if type == "grid_images":
            context = self.initiate_grid_parts(request, context)
            return JsonResponse(context)
        if type == "grid_part_list":
            context = self.get_grid_parts_list(request, context)
            return JsonResponse(context)
        if type == "grid_part_edit_form":
            context = self.get_grid_part(request, context)
        if type == "delete":
            context = self.delete_grid_part(request, context)
            return JsonResponse(context)
        if not is_ajax(request):
            context = self.initiate_grid(request, context)
            return render(request, self.template_name, context)
        return JsonResponse(context)
        
    def post(self, request, *args, **kwargs):
        context = {}
        type = request.POST.get("type")
        if type == "create":
            context = self.handle_create_grid_part(request, context)
            return JsonResponse(context)
        if type == "edit":
            context = self.handle_edit_grid_part(request, context)
            return JsonResponse(context)
        return JsonResponse(context)

    def delete_grid_part(self, request, context):
        map = request.GET.get("map")
        name = request.GET.get("name")
        grid_parts_obj = GridParts.objects.filter(map__name=map, name=name).first()
        pos_x = grid_parts_obj.position_x
        pos_y = grid_parts_obj.position_y
        context["success"] = True
        if grid_parts_obj:
            grid_parts_obj.delete()
            context["success"] = True
        if not grid_parts_obj:
            context["success"] = False
            context["error"] = "GRID PART NOT FOUND"
        grid_parts_obj = GridParts.objects.filter(map__name=map, position_x=pos_x, position_y=pos_y).first()
        context["addimage"] = False
        if grid_parts_obj:
            context["imageurl"] = grid_parts_obj.image.url
            context["addimage"] = True
        return context

    def get_grid_part(self, request, context):
        map = request.GET.get("map")
        name = request.GET.get("name")
        grid_parts_obj = GridParts.objects.filter(map__name=map, name=name)
        context["success"] = True
        if not grid_parts_obj:
            context["success"] = False
            context["error"] = "GRID PART NOT FOUND"
        context["grid_parts"] = list(grid_parts_obj.values())
        return context

    def get_grid_parts_list(self, request, context):
        map = request.GET.get("map")
        pos_x = request.GET.get("pos_x")
        pos_y = request.GET.get("pos_y")
        grid_parts_obj = GridParts.objects.filter(map__name=map, position_x=pos_x, position_y=pos_y)
        context["grid_parts"] = list(grid_parts_obj.values())
        return context

    def initiate_grid_parts(self, request, context):
        map = request.GET.get("map")
        grid_parts_obj = GridParts.objects.filter(map__name=map)
        context["grid_parts"] = list(grid_parts_obj.values())
        return context

    def handle_edit_grid_part(self, request, context):
        name = request.POST.get("name")
        map = request.POST.get("map")
        position_x = request.POST.get("pos_x")
        position_y = request.POST.get("pos_y")
        grid_part_obj = GridParts.objects.filter(name=name, map__name=map, position_x=position_x, position_y=position_y).first()
        if not grid_part_obj:
            context["error"] = "Grid Part does not exist reload page and try again."
            context["success"] = False
            return context

        grid_part_obj.width = request.POST.get("width")
        grid_part_obj.height = request.POST.get("height")
        context["imageurl"] = None
        if grid_part_obj.image:
            context["imageurl"] = grid_part_obj.image.url
        grid_part_obj.save()
        context["success"] = True
        return context

    def handle_create_grid_part(self, request, context):
        name = request.POST.get("name")
        map = request.POST.get("map")
        map_obj = MapSetup.objects.filter(name=map).first()
        if GridParts.objects.filter(name=name, map=map_obj):
            context["error"] = "This name already exists for this Grid Map"
            context["success"] = False
            return context
        grid_part_obj = GridParts.objects.create(name=name, map=map_obj)
        grid_part_obj.position_x = request.POST.get("pos_x")
        grid_part_obj.position_y = request.POST.get("pos_y")
        grid_part_obj.width = request.POST.get("width")
        grid_part_obj.height = request.POST.get("height")
        prefab_obj = PrefabsConveyor.objects.filter(name=request.POST.get("prefab")).first()
        context["imageurl"] = None
        if prefab_obj.image:
            grid_part_obj.image = prefab_obj.image
            context["imageurl"] = prefab_obj.image.url
        grid_part_obj.save()
        context["success"] = True
        return context

    def get_prefab(self, request, context):
        prefab = PrefabsConveyor.objects.filter(name=request.GET.get("prefab"))
        context["success"] = True
        if not prefab:
            context["success"] = False
            context["error"] = "Prefab no longer in database!"
        context["prefab"] = list(prefab.values())
        return context

    def populate_prefabs(self, request, context):
        prefabs = PrefabsConveyor.objects.all()
        prefab_filter = request.GET.get("filter_name")
        if prefab_filter:
            prefabs = prefabs.filter(name__icontains=prefab_filter)
        context["prefab_filter"] = prefab_filter
        context["prefabs"] = list(prefabs.values())
        return context

    def initiate_grid(self, request, context):
        name = request.GET.get("filter_name")
        map_setup = MapSetup.objects.filter(name=name).first()
        if not map_setup:
            return context
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