#!/bin/bash -xe
#
# update this script with the required migration calls

python manage.py migrate --all -v 2
