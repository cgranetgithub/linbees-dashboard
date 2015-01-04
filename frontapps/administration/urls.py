from django.conf.urls import patterns, url
from frontapps.administration import views
from frontapps.checks import noDashboardAccess,latePayment

urlpatterns = patterns('',
    url(r'^account/', views.accountAdmin, name='accountAdmin'),
    url(r'^salary/None/', views.salaryAdmin, name='salaryNone'),
    url(r'^salary/(?P<profile_id>\d+)/$', views.salaryAdmin, name='salaryEdit'),
    url(r'^task/new/', views.taskAdmin, name='taskNew'),
    url(r'^task/(?P<task_id>\d+)/$', views.taskAdmin, name='taskEdit'),
    url(r'^workspace/', views.workspaceAdmin, name='workspaceAdmin'),
    url(r'^latepayment/' , latePayment, name='latePayment'),
    url(r'^noDashboardAccess/' , noDashboardAccess, name='noDashboardAccess'),
    )
