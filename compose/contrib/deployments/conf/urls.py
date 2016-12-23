from django.conf import settings
from django.conf.urls import include, url

from  compose.core.scopes import urls as scopes_urls

urlpatterns = [
    url(r'', include(scopes_urls)),
]


