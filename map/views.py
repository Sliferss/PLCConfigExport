from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from .models import PrefabsConveyor, MapSetup, GridParts

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
    queryset = PrefabsConveyor.objects.all()

    def get(self, request, *args, **kwargs):
        context = {}
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
        if type == "create":
            context, name = self.name_check(request, context)
            prefab_obj = PrefabsConveyor.objects.filter(name=name).first()
            if prefab_obj:
                context["error"] = "Prefab Name Exist!"
                return JsonResponse(context)
            self.handle_create(request)

    def name_check(self, request, context):
        name = request.GET.get("name")
        if not name:
            context["error"] = True
        return context, name

    def handle_update(self, request, prefab_obj):
        pass

    def handle_create(self, request):
        pass