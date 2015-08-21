import compose
import os

from compose.contrib import deployments
from importlib import import_module
from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand
from django.utils.crypto import get_random_string


class Command(TemplateCommand):
    help = ("Creates a Compose deployment directory structure for the given "
            "deployment name in the current directory or optionally in the "
            "given directory.")
    missing_args_message = "You must provide a deployment name."

    def handle(self, **options):
        deployment_name, target, template = options.pop('name'), options.pop('directory'), options.pop('template')

        # validate_name method is hard-coded to handle only 'app' or 'project' strings
        # provided in the 'app_or_project' argument. However, those strings are used only
        # in the error messages and, so that the 'deployment' string is also valid.

        self.validate_name(deployment_name, "deployment")

        # if some directory is given, make sure it's nicely expanded
        if target is None:
            top_dir = os.path.join(compose.__path__[0], '..', 'deployments', deployment_name)
            try:
                os.makedirs(top_dir)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    message = "'%s' already exists" % top_dir
                else:
                    message = e
                raise CommandError(message)
            target = top_dir

            
        # Determines where the deployment templates are.
        # Use compose.__path__[0] as the default because we don't
        # know into which directory Django has been installed.
        # 
        if template is None:
            options['template'] = os.path.join(deployments.__path__[0], 'conf', 'deployment_template')


        # Check that the project_name cannot be imported.
        try:
            import_module(deployment_name)
        except ImportError:
            pass
        else:
            raise CommandError("%r conflicts with the name of an existing "
                               "Python module and cannot be used as a "
                               "deployment name. Please try another name." %
                               deployment_name)

        # Create a random SECRET_KEY to put it in the main settings.
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        options['secret_key'] = get_random_string(50, chars)

        super(Command, self).handle('deployment', deployment_name, target, **options)
