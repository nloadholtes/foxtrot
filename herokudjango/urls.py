from django.conf.urls import patterns, include, url
from django.conf import settings
from personal_api.views import AboutView, getTweets

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'herokudjango.views.home', name='home'),
    # url(r'^herokudjango/', include('herokudjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin_for_realz/', include(admin.site.urls)),
    url(r'^admin/', include('admin_honeypot.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^personal_api/$', AboutView.as_view()),
    url(r'^personal_api/getTweets', getTweets),
)

