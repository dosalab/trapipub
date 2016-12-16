#! /bin/bash

NAME="tracker"
DJANGODIR=/home/ubuntu/current
LOCAL_ADDR='127.0.0.1:8080'
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=tracker.settings
DJANGO_WSGI_MODULE=tracker.wsgi


echo "Starting $NAME as `whoami`"
cd $DJANGODIR
source /home/ubuntu/track_env/bin/activate
export DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
     --name $NAME \
     --workers $NUM_WORKERS \
     --bind=${LOCAL_ADDR} \
     --log-level=debug \
     --log-file=-
