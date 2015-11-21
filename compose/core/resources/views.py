from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
import json


class ResourceView(View):

    def get_resource(self, *args, **kwargs):
        return get_object_or_404(
            apps.get_model('resources.Resource'),
            name=kwargs['resource_name']
        )

    def options(self, request, *args, **kwargs):
        resource = self.get_resource(*args, **kwargs)
        resp = {
            'name': resource.name,
            'verbose_name': resource.verbose_name,
        }
        return HttpResponse(json.dumps(resp), content_type='application/json')
