from django.conf.urls import patterns, url
from frontapps.website import views

urlpatterns = patterns('',
    url(r'^$'        , views.home , name='home'),
    url(r'^dashboard'  , views.dashboard , name='dashboard'),
    url(r'^pricing'  , views.pricing , name='pricing'),
    url(r'^apps'     , views.apps , name='apps'),
    url(r'^about'    , views.about , name='about'),
    url(r'^contact'  , views.ContactView.as_view() , name='contact'),
    url(r'^legal'    , views.legal , name='legal'),
)
