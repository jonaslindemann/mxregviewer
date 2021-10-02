#!/bin/sh
export FLASK_ENV=production
export FLASK_APP=/home/rocky/Development/regviewer/regviewer.py
/usr/local/bin/flask run --host=0.0.0.0
