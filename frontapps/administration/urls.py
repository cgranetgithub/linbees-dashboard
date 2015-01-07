from django.conf.urls import patterns, url
from frontapps.administration import views
from frontapps.checks import noAccess,latePayment

urlpatterns = patterns('',
    url(r'^account/', views.accountAdmin, name='accountAdmin'),
    url(r'^task/new/', views.taskAdmin, name='taskNew'),
    url(r'^task/(?P<task_id>\d+)/$', views.taskAdmin, name='taskEdit'),
    url(r'^workspace/', views.workspaceAdmin, name='workspaceAdmin'),
    url(r'^latepayment/' , latePayment, name='latePayment'),
    url(r'^noAccess/' , noAccess, name='noAccess'),
    )
