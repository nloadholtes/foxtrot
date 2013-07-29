# Create your views here.
import json
import logging
import os

from django.http import HttpResponse
from django.views.generic import TemplateView
import oauth2 as oauth
import requests


log = logging.getLogger()

CACHE = {}


class AboutView(TemplateView):
    template_name = "personal_api/about.html"


def oauth_req(url, key, secret, http_method="GET", post_body=None,
        http_headers=None):
    consumer = oauth.Consumer(key=os.environ["CONSUMER_KEY"], secret=os.environ["CONSUMER_SECRET"])
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)

    resp, content = client.request(
        url,
        method=http_method,
        body=post_body,
        headers=http_headers,
    )
    return content


def getTweets(request):
    home_timeline = oauth_req(
        'https://api.twitter.com/1.1/statuses/home_timeline.json',
        os.environ['ACCESS_TOKEN'],
        os.environ['ACCESS_SECRET'],
        post_body="Nothing to see here"
    )
    # url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    return HttpResponse(json.dumps(home_timeline), content_type="application/json")


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
