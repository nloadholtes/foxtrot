# Create your views here.
import json
import logging
import os

from django.http import HttpResponse
from django.views.generic import TemplateView
import requests
from requests_oauthlib import OAuth1Session

log = logging.getLogger()

CACHE = {}


class AboutView(TemplateView):
    template_name = "personal_api/about.html"


def getTweets(request):
    twitter = OAuth1Session(resource_owner_key=os.environ['ACCESS_TOKEN'],
                            resource_owner_secret=os.environ['ACCESS_SECRET'],
                            client_key=os.environ['CONSUMER_KEY'],
                            client_secret=os.environ['CONSUMER_SECRET'],)
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    r = twitter.get(url)
    return HttpResponse(r.content, content_type="application/json")


def _setUserInfo(userinfo, requestdata):
    userinfo["etag"] = requestdata.headers["etag"]
    userinfo["output"] = requestdata.json()


def getGitHubEvents(request, user):
    log.debug("User-> %s" % user)
    userinfo = CACHE.get(user, {})
    #Update user cache if it isn't there
    if len(userinfo) == 0:
        requestdata = requests.get('https://api.github.com/users/%s/events' % user)
        _setUserInfo(userinfo, requestdata)
        CACHE[user] = userinfo

    #Github has requested that everyone honor the etag
    headers = {"If-None-Match": userinfo["etag"]}
    requestdata = requests.get('https://api.github.com/users/%s/events' % user, headers=headers)
    if requestdata.status_code != 304:
        _setUserInfo(userinfo, requestdata)
        CACHE[user] = userinfo

    output = userinfo["output"]

    return HttpResponse(json.dumps(output), content_type="application/json")
