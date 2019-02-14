#!/bin/bash

CMD=$1
PID_FILE=/opt/django/personalpage/personalpage.pid
. /opt/rh/rh-python35/enable

if [ "$CMD" == "start" ]; then
  echo "Starting gunicorn..."
  /opt/rh/rh-python35/root/usr/bin/gunicorn --workers 3 --bind unix:/opt/django/personalpage/personalpage.sock personalpage.wsgi:application --pid $PID_FILE
elif [ "$CMD" == "stop" ]; then
  echo "Stopping gunicorn..."
  /bin/kill -HUP $(cat $PID_FILE)
elif [ "$CMD" == "restart" ]; then
  echo "Restarting gunicorn..."
  if [ -f $PID_FILE ]; then
    /bin/kill -HUP $(cat $PID_FILE)
  fi
  /opt/rh/rh-python35/root/usr/bin/gunicorn --workers 3 --bind unix:/opt/django/personalpage/personalpage.sock personalpage.wsgi:application --pid $PID_FILE
else 
  echo "invalid service option.  Please use start, restart, or stop"
fi
