#!/bin/bash

sudo usermod -a -G nginx $(logname)
sudo chmod 775 /usr/share/nginx/html/django/static/blog/uploads
