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


def _setUserInfo(userinfo, requestdata):
    userinfo["etag"] = requestdata.headers["etag"]
    userinfo["output"] = requestdata.json()


def getGitHubEvents(request, user):
    log.debug("User-> %s" % user)
    userinfo = CACHE.get(user, {})
    #Update user cache if it isn't there
    if len(userinfo) == 0:
        print("Getting fresh user data")
        requestdata = requests.get('https://api.github.com/users/%s/events' % user)
        _setUserInfo(userinfo, requestdata)
        CACHE[user] = userinfo

    #Github has requested that everyone honor the etag
    headers = {"If-None-Match": userinfo["etag"]}
    requestdata = requests.get('https://api.github.com/users/%s/events' % user, headers=headers)
    if requestdata.status_code != 304:
        print("User info has updated")
        _setUserInfo(userinfo, requestdata)
        CACHE[user] = userinfo

    output = userinfo["output"]

    return HttpResponse(json.dumps(output), content_type="application/json")
