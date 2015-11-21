from django.conf import settings
from django.conf.urls import include, url

import views

urlpatterns = [
    url(r'^(?P<resource_name>[-\w]+)/$', views.ResourceView.as_view()),
    url(r'^(?P<resource_name>[-\w]+)/(?P<arguments>.+)/$', views.ResourceView.as_view()),
]
