from django.conf.urls import patterns, url
from frontapps.dashboard import views

urlpatterns = patterns('',
    url(r'^$'           , views.overview, name='overview'),
    #url(r'^analysis/'   , views.analysis, name='analysis'),
    url(r'^latepayment/', views.latePayment, name='latePayment'),
    url(r'^activities/'   , views.activities, name='activities'),
    url(r'^users/'      , views.users, name='users'),
    url(r'^logout/'     , views.logout_view, name='logout_view'),
    )
