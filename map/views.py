from django.shortcuts import render
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