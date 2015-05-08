from django.conf.urls import patterns, include, url
from applications.dashboard.views.main_page import BlankView
from django.contrib import admin
from tastypie.api import Api
from task.api import TaskResource
from record.api import RecordResource
from preference.api import PreferenceResource

v1_api = Api(api_name='v1')
#v1_api.register(UserResource())
v1_api.register(TaskResource())
v1_api.register(RecordResource())
v1_api.register(PreferenceResource())


urlpatterns = patterns('',
    url(r''         , include('applications.dashboard.urls')),
    url(r'^administration/', include('applications.administration.urls', namespace="administration")),
    url(r'^signup/'   , include('applications.signup.urls', namespace="signup")),
    url(r'^clientapp/', include('applications.clientapp.urls', namespace="clientapp")),
    url(r'^api/'      , include(v1_api.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
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
