#!/bin/bash
exec gunicorn -w 20 --timeout=30 -b 0.0.0.0:8111 start_kmv_api_g1:app
