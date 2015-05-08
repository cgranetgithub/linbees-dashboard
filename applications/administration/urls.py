from django.conf.urls import patterns, url
from applications.administration import views
from applications.checks import noAccess,latePayment

urlpatterns = patterns('',
    url(r'^account/', views.accountAdmin, name='accountAdmin'),
    url(r'^workspace/', views.workspaceAdmin, name='workspaceAdmin'),
    )
