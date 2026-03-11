#!/bin/bash

set -e
chalice local --port=7415 --host=0.0.0.0 && /usr/sbin/nginx -g 'daemon off;'
