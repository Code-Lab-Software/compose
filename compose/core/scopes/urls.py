from compose.core.scopes import views

from django.apps import apps
from django.conf import settings
from django.conf.urls import include, url

urlpatterns = []
for resource in apps.get_model('scopes', 'Resource').objects.all():
    kwargs = ["(?P<%s>%s)" % (identifier.name, identifier.regex) for identifier in resource.identifiers.all()]
    data = {'resource_name': resource.name}
    if kwargs:
        pth = r'^%(resource_name)s/%(kwargs)s/$'
        data['kwargs'] = '/'.join(kwargs)
    else:
        pth = r'^%(resource_name)s/$'
    urlpatterns.append(url(pth % data, views.ResourceView.as_view(resource_name=resource.name),))


