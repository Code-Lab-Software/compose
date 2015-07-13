import os
import settings_tools
import sys

from django.utils.crypto import get_random_string

COMPOSE_SETTINGS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add some required paths to the sys.path list. The paths
# are constructed relatively to this module location 
PATH_PREFIX = os.path.split(COMPOSE_SETTINGS_PATH)[0]
for pth in ('%s/../', '%s/modules', '%s/deployments'):
    sys.path.append(pth % PATH_PREFIX)    

# Dynamically load and merge settings modules. The name of the 
# `sitesettings` module is provided dynamically via the env variable
settings_modules = ('django.conf.global_settings', 'compose.conf.global_settings', 'compose.conf.custom_settings')
DEPLOYMENT = None
if os.environ.has_key('DEPLOYMENT'):
    DEPLOYMENT = os.environ['DEPLOYMENT']
    settings_modules = settings_modules + ('%s.conf.settings' % DEPLOYMENT,)
settings_tools.merge_settings(globals(), *settings_modules)
if DEPLOYMENT is None:
    # If the DEPLOYMENT mode is off there is no local deployment
    # settings.py file provided. Thus, to initialize the `compose.core.management`
    # commands (i.e. to activate startdeployment command) we have to simulate the SECRET_KEY,
    # as this is required by Django.
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    SECRET_KEY = get_random_string(50, chars)

# ---------------------------
# Now we have all default and the 
# custom settings loaded - let's process them..
# ---------------------------

# Add the custom python paths to the sys.path
for pth in DEP_PYTHON_PATHS:
    sys.path.append(pth % PATH_PREFIX)    

# And build up some special settings out of the custom components
DATABASE_ROUTERS = DEP_DATABASE_ROUTERS['HEAD'] +  DATABASE_ROUTERS + DEP_DATABASE_ROUTERS['TAIL']
INSTALLED_URLS = DEP_INSTALLED_URLS['HEAD'] + INSTALLED_URLS + DEP_INSTALLED_URLS['TAIL']
MIDDLEWARE_CLASSES = DEP_MIDDLEWARE_CLASSES['HEAD'] + MIDDLEWARE_CLASSES + DEP_MIDDLEWARE_CLASSES['TAIL']
INSTALLED_APPS = DEP_INSTALLED_APPS['HEAD'] + INSTALLED_APPS + DEP_INSTALLED_APPS['TAIL']
AUTHENTICATION_BACKENDS = DEP_AUTHENTICATION_BACKENDS['HEAD'] + AUTHENTICATION_BACKENDS + DEP_AUTHENTICATION_BACKENDS['TAIL']

