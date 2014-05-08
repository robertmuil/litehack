from django.conf.urls import patterns, url

from battstat import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^batt_raw$', views.batt_raw, name='batt_raw'),
)
