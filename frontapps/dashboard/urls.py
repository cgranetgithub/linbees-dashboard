from django.conf.urls import patterns, url
from frontapps.dashboard import views
from frontapps.checks import noDashboardAccess,latePayment

urlpatterns = patterns('',
    url(r'^$'            , views.overview, name='overview'),
    #url(r'^analysis/'   , views.analysis, name='analysis'),
    url(r'^latepayment/' , latePayment, name='latePayment'),
    url(r'^noDashboardAccess/' , noDashboardAccess, name='noDashboardAccess'),
    url(r'^time/'        , views.time, name='time'),
    url(r'^cost/'        , views.cost, name='cost'),
    url(r'^gettasks/'        , views.get_tasks, name='gettasks'),
    url(r'^user/'        , views.user, name='user'),
    url(r'^logout/'      , views.logout_view, name='logout_view'),
    url(r'^data/time_per_project/', views.data_time_per_project, name='data_time_per_project'),
    url(r'^data/cost_per_project/', views.data_cost_per_project, name='data_cost_per_project'),
    url(r'^data/cumulated_time_per_project/', views.data_cumulated_time_per_project, name='data_cumulated_time_per_project'),
    url(r'^data/cumulated_cost_per_project/', views.data_cumulated_cost_per_project, name='data_cumulated_cost_per_project'),
    )
