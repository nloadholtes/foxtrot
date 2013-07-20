# Create your views here.
import json

from django.views.generic import TemplateView
from django.http import HttpResponse
import requests
import logging

log = logging.getLogger()

CACHE = {}

class AboutView(TemplateView):
    template_name = "personal_api/about.html"


def getTweets(request):
    output = {}
    return HttpResponse(json.dumps(output), content_type="application/json")


def getGitHubEvents(request, user):
    log.debug("User-> %s" % user)
    #Do we have user info
    userinfo = CACHE.get(user, {})
    #Is it current
    if len(userinfo) == 0:
        print("Getting fresh user data")
        requestdata = requests.get('https://api.github.com/users/%s/events' % user)
        userinfo["etag"] = requestdata.headers["etag"]
        output = requestdata.json()
    #Is it a 304
   

    output = requests.get('https://api.github.com/users/%s/events' % user).json()

    return HttpResponse(json.dumps(output), content_type="application/json")
