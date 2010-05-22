#!/bin/bash -xe
#
# update this script with the required migration calls

python manage.py migrate basic_groups 0001 --fake
python manage.py migrate tribes 0001 --fake
python manage.py migrate projects 0001 --fake

python manage.py migrate --all -v 2
