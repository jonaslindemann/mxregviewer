#!/bin/sh
export FLASK_ENV=production
export FLASK_APP=/home/pi/Development/mxregviewer/regviewer.py
export FLASK_CMD=/usr/bin/flask

$FLASK_CMD run --host=0.0.0.0
