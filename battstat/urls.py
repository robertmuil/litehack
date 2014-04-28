from django.conf.urls import patterns, url

from battstat import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
