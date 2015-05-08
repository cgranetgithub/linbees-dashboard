from django.conf.urls import patterns, url
from applications.signup import views

urlpatterns = patterns('',
    url(r'^$'     , views.signup, name='signup'),
)
