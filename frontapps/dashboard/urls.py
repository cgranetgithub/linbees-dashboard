from django.conf.urls import patterns, url
from frontapps.dashboard import views

urlpatterns = patterns('',
    url(r'^$'            , views.overview, name='overview'),
    #url(r'^analysis/'   , views.analysis, name='analysis'),
    url(r'^latepayment/' , views.latePayment, name='latePayment'),
    url(r'^time/'        , views.time, name='time'),
    url(r'^activity/new/', views.activityAdmin , name='activityNew'),
    url(r'^activity/(?P<activity_id>\d+)/$', views.activityAdmin , name='activityEdit'),
    #url(r'^users/'      , views.users, name='users'),
    url(r'^logout/'      , views.logout_view, name='logout_view'),
    )
