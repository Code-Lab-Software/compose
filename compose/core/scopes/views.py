from django.apps import apps
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
import json


class ResourceView(View):
    resource_name = None

    def __init__(self, **kwargs):
        super(ResourceView, self).__init__(**kwargs)
        # cache resource object initially
        self.resource = self.get_resource()
    
    def dispatch(self, *args, **kwargs):
        return super(ResourceView, self).dispatch(*args, **kwargs)

    def get_resource(self):
        return get_object_or_404(
            apps.get_model('scopes.Resource'),
            name=self.resource_name
        )

    def get(self, request, *args, **kwargs):
        resp = {
            'name': self.resource_name,
            'verbose_name': self.resource.verbose_name,
        }
        return HttpResponse(json.dumps(resp), content_type='application/json')
