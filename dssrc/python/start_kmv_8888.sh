#!/bin/bash
exec gunicorn -w 3 --timeout=30 -b 0.0.0.0:8888 start_kmv_api_g1:app
#nohup exec gunicorn -w 3 --timeout=30 -b 0.0.0.0:8888 start_kmv_api_g1:app 1>/dev/null 2>&1 &
