from django.conf.urls import patterns, url
from frontapps.dashboard import views, queries
from frontapps.checks import noAccess,latePayment

urlpatterns = patterns('',
    url(r'^$'            , views.overview, name='overview'),
    #url(r'^analysis/'   , views.analysis, name='analysis'),
    url(r'^latepayment/' , latePayment, name='latePayment'),
    url(r'^noAccess/'    , noAccess, name='noAccess'),
    url(r'^time/'        , views.time, name='time'),
    url(r'^cost/'        , views.cost, name='cost'),
    url(r'^user/time/'   , views.user_time  , name='user_time'),
    url(r'^user/info/'   , views.user_info  , name='user_info'),
    url(r'^user/salary/' , views.user_salary, name='user_salary'),
    url(r'^edit/info/(?P<user_id>\d+)/$'  , views.user_info_edit  , name='edit_info'),
    url(r'^edit/salary/(?P<user_id>\d+)/$', views.user_salary_edit, name='edit_salary'),
    #url(r'^edit/workspace/', views.edit_salary     , name='edit_workspace'),
    url(r'^logout/'      , views.logout_view, name='logout_view'),
    url(r'^data/users/'  , queries.users, name='users_query'),
    url(r'^data/tasks/'  , queries.tasks, name='tasks_query'),
    url(r'^data/time_per_user/', queries.time_per_user, name='time_per_user_query'),
    url(r'^data/time_per_project/', queries.time_per_project, name='time_per_project_query'),
    url(r'^data/cost_per_project/', queries.cost_per_project, name='cost_per_project_query'),
    url(r'^data/cumulated_time_per_project/', queries.cumulated_time_per_project, name='cumulated_time_per_project_query'),
    url(r'^data/cumulated_cost_per_project/', queries.cumulated_cost_per_project, name='cumulated_cost_per_project_query'),
    )
