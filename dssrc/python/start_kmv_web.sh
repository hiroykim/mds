#!/bin/bash
exec gunicorn -w 4 --timeout=3 -b 0.0.0.0:8888 start_kmv_api:app
