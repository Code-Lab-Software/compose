from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = []

# Load urls registed in URL_APPS custom Compose INSTALLED_URLS variable
for app in settings.INSTALLED_URL_APPS:
    modl  = __import__('%s.urls' % (app,), globals(), locals(), [], -1)
    urlpatterns += url(r'', include('%s.urls' % (app,)))

# If the DEBUG mode is on, add static files server urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

