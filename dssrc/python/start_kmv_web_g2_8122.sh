#!/bin/bash
exec gunicorn -w 10 --timeout=3 -b 0.0.0.0:8122 start_kmv_api_g2:app
