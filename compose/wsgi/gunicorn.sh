#!/bin/bash

# NAME -  Name of the application
# DJANGODIR - Django project directory
# USER - the user to run as
# GROUP -  the group to run as
# NUM_WORKERS - how many worker processes should Gunicorn spawn
# VENV_DIR - virtual env dir
# COMPOSEPROFILE - compose profile name
# IP - IP address to bind
# PORT - PORT to bind
# TIMEOUT - timeout

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $VENV_DIR
source ./bin/activate 

# Jump to djangodir
cd $DJANGODIR
export DEPLOYMENT=$DEPLOYMENT

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec  gunicorn compose.wsgi.wsgi:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=${IP}:${PORT} \
  --timeout $TIMEOUT \
#  --log-level=debug \
  --log-file=-

