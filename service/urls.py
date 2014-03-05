from django.conf.urls import patterns, include, url
from frontapps.website.views import BlankView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from libs.api.resources import (ActivityResource, RecordResource,
				PreferenceResource, CloseLastRecordResource)

v1_api = Api(api_name='v1')
#v1_api.register(UserResource())
v1_api.register(ActivityResource())
v1_api.register(RecordResource())
v1_api.register(CloseLastRecordResource())
v1_api.register(PreferenceResource())


urlpatterns = patterns('',
    url(r'^$'         , 'frontapps.website.views.home', name="home"),
    url(r'^administration/', include('frontapps.administration.urls', namespace="administration")),
    url(r'^dashboard/', include('frontapps.dashboard.urls', namespace="dashboard")),
    url(r'^website/'  , include('frontapps.website.urls', namespace="website")),
    url(r'^signup/'   , include('frontapps.signup.urls', namespace="signup")),
    url(r'^clientapp/', include('frontapps.clientapp.urls', namespace="clientapp")),
    url(r'^api/'      , include(v1_api.urls)),
    url(r'^dashboard/login/$', 'django.contrib.auth.views.login'),
    url(r'^blank/'   , BlankView.as_view(), name="blank"),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n')),    
)
