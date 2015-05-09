from django.conf.urls import patterns, url
from pages.signup import views

urlpatterns = patterns('',
    url(r'^$'     , views.signup, name='signup'),
)
