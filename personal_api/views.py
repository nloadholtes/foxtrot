# Create your views here.
import json

from django.views.generic import TemplateView
from django.http import HttpResponse
import requests


class AboutView(TemplateView):
    template_name = "personal_api/about.html"


def getTweets(request):
    output = {}
    return HttpResponse(json.dumps(output), content_type="application/json")


def getGitHubEvents(request, user):
    output = requests.get('https://api.github.com/users/%s/events' % user).json()

    return HttpResponse(json.dumps(output), content_type="application/json")
