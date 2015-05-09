from django.conf.urls import patterns, url
from pages.administration import views
from pages.checks import noAccess,latePayment

urlpatterns = patterns('',
    url(r'^account/', views.accountAdmin, name='accountAdmin'),
    url(r'^workspace/', views.workspaceAdmin, name='workspaceAdmin'),
    )
