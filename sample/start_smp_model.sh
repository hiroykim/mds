#!/bin/bash
exec gunicorn -w 1 --timeout=30 -b 0.0.0.0:8000 wsgi:app
