from django.conf.urls import patterns, url
from frontapps.administration import views
from frontapps.checks import noAccess,latePayment

urlpatterns = patterns('',
    url(r'^account/', views.accountAdmin, name='accountAdmin'),
    url(r'^workspace/', views.workspaceAdmin, name='workspaceAdmin'),
    )
