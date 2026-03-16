#!/bin/bash

set -e
#python manage.py runserver 0.0.0.0:7415 && /usr/sbin/nginx -g 'daemon off;'
uvicorn main:app --reload --host 0.0.0.0 --port 7415
