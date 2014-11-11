from django.conf.urls import patterns, url
from frontapps.signup import views

urlpatterns = patterns('',
    url(r'^$'     , views.signup, name='signup'),
)
