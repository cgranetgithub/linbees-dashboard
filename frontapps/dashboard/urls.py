from django.conf.urls import patterns, url
from frontapps.dashboard import views

urlpatterns = patterns('',
    url(r'^$'            , views.overview, name='overview'),
    #url(r'^analysis/'   , views.analysis, name='analysis'),
    url(r'^latepayment/' , views.latePayment, name='latePayment'),
    url(r'^time/'        , views.time, name='time'),
    url(r'^task/new/', views.taskAdmin , name='taskNew'),
    url(r'^task/(?P<task_id>\d+)/$', views.taskAdmin , name='taskEdit'),
    #url(r'^users/'      , views.users, name='users'),
    url(r'^logout/'      , views.logout_view, name='logout_view'),
    url(r'^data/time_per_project/(?P<startdate>[\w\-]+)/(?P<enddate>[\w\-]+)/$', views.data_time_per_project, name='data_time_per_project'),
    url(r'^data/cumulated_time_per_project/(?P<startdate>[\w\-]+)/(?P<enddate>[\w\-]+)/$', views.data_cumulated_time_per_project, name='data_cumulated_time_per_project')
    )
