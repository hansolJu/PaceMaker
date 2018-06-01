from django.http import HttpResponse

# Create your views here.
from django.views import View


class diagramBV(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')