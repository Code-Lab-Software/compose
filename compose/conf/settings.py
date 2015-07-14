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
#settings_modules = ('django.conf.global_settings', 'compose.conf.global_settings', 'compose.conf.custom_settings')
settings_modules = ('compose.conf.global_settings', 'compose.conf.custom_settings')
settings_tools.merge_settings(globals(), *settings_modules)

#To initialize the `compose.core.management`
# commands (i.e. to activate startdeployment command) we have to simulate the SECRET_KEY,
# as this is required by Django.
chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = get_random_string(50, chars)



