from django.conf.urls import patterns, url

from .basic_navigation import views
from .basic_navigation import api

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^api/(?P<project_identifier>\w+)/', api.save_score, name="save_score"),
)
