from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from .models import PrefabsConveyor, MapSetup, GridParts
from django.utils.crypto import get_random_string
from .models import PrefabsConveyor
import os
from django.conf import settings

def is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


class Index(View):
    template_name = "map_index.html"

    def get(self, request, *args, **kwargs):
        context = {}
        if not is_ajax(request):
            return render(request, self.template_name, context)


class PrefabsView(View):
    template_name = "prefabs_view.html"

    def post(self, request, *args, **kwargs):
        context = {}
        context["error"] = False
        self.name = request.POST.get('name')
        if not self.name:
            context["error"] = "Missing Name!"
            return JsonResponse(context)
        self.type = request.POST.get('type')
        self.length = request.POST.get('length')
        self.width = request.POST.get('width')
        self.height = request.POST.get('height')
        self.image = request.FILES.get('image')
        if self.type == "create":
            context = self.handle_create(context)
        return JsonResponse(context)

    def get(self, request, *args, **kwargs):
        context = {}
        self.queryset = PrefabsConveyor.objects.all()
        if not is_ajax(request):
            context["prefabs"] = self.queryset
            return render(request, self.template_name, context)

        type = request.GET.get("type")
        if type == "modal_get":
            context, name = self.name_check(request, context)
            prefab_obj = PrefabsConveyor.objects.filter(name=name)
            if not prefab_obj:
                context["error"] = "Prefab Doesn't Exist!"
                return JsonResponse(context)
            context["prefab"] = list(prefab_obj.values())
            return JsonResponse(context)
        if type == "update":
            context, name = self.name_check(request, context)
            prefab_obj = PrefabsConveyor.objects.filter(name=name).first()
            if not prefab_obj:
                context["error"] = "Prefab Doesn't Exist!"
                return JsonResponse(context)
            context = self.handle_update(request, prefab_obj)

    def name_check(self, request, context):
        name = request.GET.get("name")
        if not name:
            context["error"] = True
        return context, name

    def handle_update(self, request, prefab_obj):
        pass

    def handle_create(self, context):
        if PrefabsConveyor.objects.filter(name=self.name):
            context["error"] = "Name Already Exists!"
            return context
        create_obj = PrefabsConveyor.objects.create(name=self.name)
        if self.length:
            create_obj.length = self.length
        if self.width:
            create_obj.width = self.width
        if self.height:
            create_obj.height = self.height
        if self.image:
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
            print(image_path)
            create_obj.image = image_path
            create_obj.save()
        create_obj.save()
        context["success"] = "Created Prefab: " + self.name
        return context