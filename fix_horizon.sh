#!/bin/bash

# This script is used to fix horizon auth table problem

HORIZON_PATH=/opt/stack.kilo/horizon

cd $HORIZON_PATH
python manage.py makemigrations
python manage.py migrate
