from django.apps import apps
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
import json


class ResourceView(View):

    def dispatch(self, *args, **kwargs):
        return super(ResourceView, self).dispatch(*args, **kwargs)

    def get_resource(self, *args, **kwargs):
        return get_object_or_404(
            apps.get_model('resources.Resource'),
            name=kwargs.get('resource_name')
        )

    def check_arguments(self, *args, **kwargs):
        if kwargs.get('arguments', None):
            resource_arguments = kwargs.get('arguments').split('/')
            if len(resource_arguments) != self.get_resource(*args, **kwargs).resourceargument_set.count():
                raise Http404
        elif self.get_resource(*args, **kwargs).resourceargument_set.count() != 0:
            raise Http404

    def get_arguments(self, *args, **kwargs):
        if self.kwargs.get('arguments'):
            self.check_arguments(*args, **kwargs)
            argument_providers = apps.get_model('providers.ResourceStateArgumentProvider').objects.filter(resource_argument__resource=self.get_resource(*args, **kwargs))
            arguments = self.get_resource(*args, **kwargs).resourceargument_set.filter(resourcestateargumentprovider__in=argument_providers)
            print 'arg_prov:', argument_providers
            print 'arguments:', arguments
            local_kwargs = {}
            for argument_provider in argument_providers:
                print 'kwargs', kwargs
                print 'name', argument_provider.resource_argument.name
                #local_kwargs[argument_provider.node_state_argument.get_object().name] = self.kwargs.get(argument_provider.resource_argument.name)
                local_kwargs[argument_provider.node_state_argument.get_object().name] = self.kwargs.get('arguments')
            return local_kwargs
            return dict(zip(arguments, self.kwargs.get('arguments').split('/')))
        return None
        
    def options(self, request, *args, **kwargs):
        self.check_arguments(*args, **kwargs)
        resource = self.get_resource(*args, **kwargs)
        resp = {
            'name': resource.name,
            'verbose_name': resource.verbose_name,
            'nodes': [],
        }
        for node in resource.branch.nodes.all():
            resp['nodes'].append(node.get_object().name)
        return HttpResponse(json.dumps(resp), content_type='application/json')

    def get(self, request, *args, **kwargs):
        self.check_arguments(*args, **kwargs)
        nid = request.GET.get('nid', None)
        if nid:
            # we have Node ID so it is request for node:
            node = get_object_or_404(
                apps.get_model('scopes.Node'),
                id=nid
            )
            print 'lala', self.get_arguments(*args, **kwargs)
            node_val = node.get(**self.get_arguments(*args, **kwargs))
            try:
                resp = json.dumps(node_val)
            except TypeError, e:
                ret = {}
                for k, v in node_val.iteritems():
                    ret[k] = u'%s' % v
                resp = json.dumps(ret)
            return HttpResponse(resp, content_type='application/json')
        else:
            # request for whole branch
            return HttpResponse(json.dumps({'title': "I'm the BRANCH biiiiiatch!", 'content': 'What would you like to do?'}), content_type='application/json')
