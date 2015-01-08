from django.conf.urls import patterns, url
from frontapps.dashboard import views, queries
from frontapps.checks import noAccess,latePayment

urlpatterns = patterns('',
    url(r'^$'           , views.main.overview, name='overview'),
    url(r'^logout/'     , views.main.logout_view, name='logout_view'),
    url(r'^latepayment/', latePayment, name='latePayment'),
    url(r'^noAccess/'   , noAccess, name='noAccess'),
    url(r'^task/time/'  , views.task.time, name='task_time'),
    url(r'^task/cost/'  , views.task.cost, name='task_cost'),
    url(r'^task/info/'  , views.task.info, name='task_info'),
    url(r'^task/edit/info/(?P<task_id>\d+)/$', views.task.info_edit, name='task_info_edit'),
    url(r'^user/time/'  , views.user.time  , name='user_time'),
    url(r'^user/info/'  , views.user.info  , name='user_info'),
    url(r'^user/salary/', views.user.salary, name='user_salary'),
    url(r'^user/edit/info/(?P<user_id>\d+)/$'  , views.user.info_edit  , name='user_info_edit'),
    url(r'^user/edit/salary/(?P<user_id>\d+)/$', views.user.salary_edit, name='user_salary_edit'),
    url(r'^data/users/', queries.users, name='users_query'),
    url(r'^data/tasks/', queries.tasks, name='tasks_query'),
    url(r'^data/time_per_user/'   , queries.time_per_user, name='time_per_user_query'),
    url(r'^data/time_per_project/', queries.time_per_project, name='time_per_project_query'),
    url(r'^data/cost_per_project/', queries.cost_per_project, name='cost_per_project_query'),
    url(r'^data/cumulated_time_per_project/', queries.cumulated_time_per_project, name='cumulated_time_per_project_query'),
    url(r'^data/cumulated_cost_per_project/', queries.cumulated_cost_per_project, name='cumulated_cost_per_project_query'),
    )
