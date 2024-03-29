from django.conf.urls import patterns, url
from pages.clientapp import views

urlpatterns = patterns('',
    url(r'^$'          , views.client_home    , name='home'),
    url(r'^report/'    , views.client_report  , name='report'),
    url(r'^register/'  , views.client_register, name='register'),
    url(r'^setmanager/', views.client_set_manager, name='setmanager'),
    url(r'^login/'     , views.client_login   , name='login'),
    url(r'^logout/'    , views.client_logout  , name='logout'),
    url(r'^tutorial/'  , views.client_tutorial, name='tutorial'),
    url(r'^data/tasks/'   , views.tasks   , name='tasks_query'),
    url(r'^data/managers/', views.managers, name='managers_query'),
)
