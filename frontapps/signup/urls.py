from django.conf.urls import patterns, url
from frontapps.signup import views

urlpatterns = patterns('',
    url(r'^$'     , views.signup, name='signup'),
    #url(r'^step1/', 'step1'),
    #url(r'^step2/', 'step2'),
    #url(r'^step3/', 'step3'),
    #url(r'^step4/', 'step4'),
)
