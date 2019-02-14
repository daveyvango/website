#!/bin/bash

CMD=$1
PID_FILE=/opt/django/personalpage/personalpage.pid
. /opt/rh/rh-python35/enable

if [[ "$CMD" == "start" ]]; then
  /opt/rh/rh-python35/root/usr/bin/gunicorn --workers 3 --bind unix:/opt/django/personalpage/personalpage.sock personalpage.wsgi:application --daemon --pid $PID_FILE
elif [[ "$CMD" == "stop" ]]; then
  /bin/kill -HUP $(cat $PID_FILE)
elif [[ "$CMD" == "restart" ]]; then
  /bin/kill -HUP $(cat $PID_FILE)
  /opt/rh/rh-python35/root/usr/bin/gunicorn --workers 3 --bind unix:/opt/django/personalpage/personalpage.sock personalpage.wsgi:application --daemon --pid $PID_FILE
else 
  echo "invalid service option.  Please use start, restart, or stop"
fi
