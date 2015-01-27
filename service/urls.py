from django.conf.urls import patterns, include, url
from apps.website.views import BlankView
from django.contrib import admin
from tastypie.api import Api
from apps.task.api import TaskResource
from apps.record.api import RecordResource
from apps.preference.api import PreferenceResource

v1_api = Api(api_name='v1')
#v1_api.register(UserResource())
v1_api.register(TaskResource())
v1_api.register(RecordResource())
v1_api.register(PreferenceResource())


urlpatterns = patterns('',
    url(r'^$'         , 'apps.website.views.home', name="home"),
    url(r'^administration/', include('apps.administration.urls', namespace="administration")),
    url(r'^dashboard/', include('apps.dashboard.urls', namespace="dashboard")),
    url(r'^website/'  , include('apps.website.urls', namespace="website")),
    url(r'^signup/'   , include('apps.signup.urls', namespace="signup")),
    url(r'^clientapp/', include('apps.clientapp.urls', namespace="clientapp")),
    url(r'^api/'      , include(v1_api.urls)),
    url(r'^dashboard/login/$', 'django.contrib.auth.views.login'),
    url(r'^blank/'   , BlankView.as_view(), name="blank"),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n')),    
)

import os
if os.environ.get("STAGING") == 'True':
    from django.http import HttpResponse
    urlpatterns += patterns('',
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", 
                                            content_type="text/plain"))
    )
