#!/bin/sh

WORKON_HOME=/sites
PROJECT_ROOT=/sites/anadusis

# activate virtual environment
. $WORKON_HOME/pinax-env/bin/activate

cd $PROJECT_ROOT
mkdir -p logs
python manage.py cron >> $PROJECT_ROOT/logs/cron_mail.log 2>&1