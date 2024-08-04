from django.shortcuts import render
from django.views.generic import View


def is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


class Index(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = {}
        if not is_ajax(request):
            return render(request, self.template_name, context)
