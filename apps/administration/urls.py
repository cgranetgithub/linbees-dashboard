from django.conf.urls import patterns, url
from apps.administration import views
from apps.checks import noAccess,latePayment

urlpatterns = patterns('',
    url(r'^account/', views.accountAdmin, name='accountAdmin'),
    url(r'^workspace/', views.workspaceAdmin, name='workspaceAdmin'),
    )
