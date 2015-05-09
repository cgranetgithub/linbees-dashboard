from django.conf.urls import patterns, url
#from pages.dashboard import views, queries
from pages.checks import noAccess, latePayment

urlpatterns = patterns('pages.dashboard.views',
    url(r'^$'           , 'main_page.overview', name='overview'),
    url(r'^logout/'     , 'main_page.logout_view', name='logout_view'),
    url(r'^task/time/'  , 'task_page.time', name='task_time'),
    url(r'^task/cost/'  , 'task_page.cost', name='task_cost'),
    url(r'^task/comparison/', 'task_page.comparison', name='task_comparison'),
    url(r'^task/table/' , 'task_page.comparison_table', name='task_table'),
    url(r'^task/info/'  , 'task_page.info', name='task_info'),
    url(r'^task/new/'   , 'task_page.new',  name='task_new'),
    url(r'^task/edit/info/(?P<task_id>\d+)/$', 'task_page.info_edit', name='task_info_edit'),
    url(r'^user/time/'  , 'user_page.time'  , name='user_time'),
    url(r'^user/info/'  , 'user_page.info'  , name='user_info'),
    url(r'^user/salary/', 'user_page.salary', name='user_salary'),
    url(r'^user/edit/info/(?P<user_id>\d+)/$'  , 'user_page.info_edit'  , name='user_info_edit'),
    url(r'^user/edit/salary/(?P<user_id>\d+)/$', 'user_page.salary_edit', name='user_salary_edit'),
    )

urlpatterns += patterns('pages.dashboard.queries',
    url(r'^data/users/', 'users', name='users_query'),
    url(r'^data/tasks/(?P<single>\w+)/$', 'tasks', name='tasks_query'),
    url(r'^data/time_per_user/'   , 'time_per_user', name='time_per_user_query'),
    url(r'^data/time_per_project/', 'time_per_project', name='time_per_project_query'),
    url(r'^data/cost_per_project/', 'cost_per_project', name='cost_per_project_query'),
    url(r'^data/cumulated_time_per_project/', 'cumulated_time_per_project', name='cumulated_time_per_project_query'),
    url(r'^data/cumulated_cost_per_project/', 'cumulated_cost_per_project', name='cumulated_cost_per_project_query'),
    url(r'^data/total_time_per_project/', 'total_time_per_project', name='time_repartition_query'),
    url(r'^data/total_cost_per_project/', 'total_cost_per_project', name='cost_repartition_query'),
    )

urlpatterns += patterns('',
    url(r'^latepayment/', latePayment, name='latePayment'),
    url(r'^noAccess/'   , noAccess, name='noAccess'),
    )
