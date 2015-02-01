from django.conf.urls import patterns, url
from apps.clientapp import views

urlpatterns = patterns('',
    url(r'^$'        , views.client_home    , name='home'),
    url(r'^register/', views.client_register, name='register'),
    url(r'^login/'   , views.client_login   , name='login'),
    url(r'^logout/'  , views.client_logout  , name='logout'),
    url(r'^tutorial/', views.client_tutorial, name='tutorial'),
)