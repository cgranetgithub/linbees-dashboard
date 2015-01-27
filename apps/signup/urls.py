from django.conf.urls import patterns, url
from apps.signup import views

urlpatterns = patterns('',
    url(r'^$'     , views.signup, name='signup'),
)
