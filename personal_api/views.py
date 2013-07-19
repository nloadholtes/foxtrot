# Create your views here.
import json

from django.views.generic import TemplateView
from django.http import HttpResponse


class AboutView(TemplateView):
    template_name = "personal_api/about.html"


def getTweets(request):
    output = {}
    return HttpResponse(json.dumps(output), content_type="application/json")
