from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from map.models import PrefabsConveyor
from map.views import is_ajax
from django.utils.crypto import get_random_string
from map.models import PrefabsConveyor
import os
from django.conf import settings


class PrefabsView(View):
    template_name = "prefabs_view.html"

    def post(self, request, *args, **kwargs):
        context = {}
        context["success"] = True
        context["error"] = ""
        name = request.POST.get('name')
        if not name:
            context["success"] = False
            context["error"] = "Missing Name!"
            return JsonResponse(context)
        type = request.POST.get('type')
        self.image = request.FILES.get('image')
        if type == "create":
            context = self.handle_create(request, context)
            return JsonResponse(context)
        if type == "update":
            context = self.handle_update(request, context)
            return JsonResponse(context)
        context["success"] = False
        context["error"] = "Did not reach correct method in view class"
        return JsonResponse(context)

    def get(self, request, *args, **kwargs):
        context = {}
        self.queryset = PrefabsConveyor.objects.all()
        if not is_ajax(request):
            name = request.GET.get("filter_name")
            if name:
                self.queryset = self.queryset.filter(name__icontains=name)
                context["filter_name"] = name
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

    def name_check(self, request, context):
        name = request.GET.get("name")
        if not name:
            context["error"] = True
        return context, name

    def handle_update(self, request, context):
        original_name = request.POST.get("original_name")
        name = request.POST.get('name')
        prefab_obj = PrefabsConveyor.objects.filter(name=name).first()
        if not prefab_obj:
            prefab_obj = PrefabsConveyor.objects.create(name=name)
        prefab_obj = self.fill_prefab_fields(request, prefab_obj)
        context["success"] = True
        context["error"] = "Edited Prefab " + name + "!"
        if name != original_name:
            old_obj = PrefabsConveyor.objects.filter(name=original_name)
            if old_obj:
                old_obj.delete()
        return context

    def handle_create(self, request, context):
        original_name = request.POST.get("original_name")
        name = request.POST.get('name')
        if PrefabsConveyor.objects.filter(name=name):
            context["success"] = False
            context["error"] = "Name Already Exists!"
            return context
        prefab_obj = PrefabsConveyor.objects.create(name=name)
        prefab_obj = self.fill_prefab_fields(request, prefab_obj)
        context["success"] = True
        context["error"] = "Created Prefab " + name + "!"
        return context

    def fill_prefab_fields(self, request, prefab_obj):
        rest_post = request.POST
        prefab_obj.speed1 = rest_post.get("speed1")
        prefab_obj.speed2 = rest_post.get("speed2")
        prefab_obj.speed3 = rest_post.get("speed3")
        prefab_obj.stand_by_time = rest_post.get("stand_by_time")
        prefab_obj.head_pec_fitted = False
        if rest_post.get("head_pec_fitted").lower().capitalize() == "True":
            prefab_obj.head_pec_fitted = True
        prefab_obj.tail_pec_fitted = False
        if rest_post.get("tail_pec_fitted").lower().capitalize() == "True":
            prefab_obj.tail_pec_fitted = True
        prefab_obj.head_pect_distance = rest_post.get("head_pect_distance")
        prefab_obj.tail_pect_distance = rest_post.get("tail_pect_distance")
        prefab_obj.cm_number = rest_post.get("cm_number")
        prefab_obj.encoder_fitted = False
        if rest_post.get("encoder_fitted").lower().capitalize() == "True":
            prefab_obj.encoder_fitted = True
        prefab_obj.ramp_up = rest_post.get("ramp_up")
        prefab_obj.ramp_down = rest_post.get("ramp_down")
        prefab_obj.start_position_fwd = rest_post.get("start_position_fwd")
        prefab_obj.group_id = rest_post.get("group_id")
        prefab_obj.cm_head = rest_post.get("cm_head")
        prefab_obj.cm_tail = rest_post.get("cm_tail")
        if self.image:
            prefab_obj.image = self.upload_image()
        prefab_obj.save()
        return prefab_obj

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