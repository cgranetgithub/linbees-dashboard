from django.conf.urls import patterns, url
from frontapps.administration import views

urlpatterns = patterns('',
    #url(r'^users/'     , views.userAdmin     , name='userAdmin'),
    url(r'^workspace/' , views.workspaceAdmin, name='workspaceAdmin'),
    url(r'^account/'   , views.accountAdmin  , name='accountAdmin'),
    )
