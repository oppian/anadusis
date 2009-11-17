#!/bin/bash -e
#
# Some post django install tasks, like syncdb
#
# $DEPLOY_DIR  -- Installed directory
# $HOSTNAME    -- Hostname of server
# $APP_OWNER   -- User to chmod the files in deploy dir
#
# pkgs: flip

#
# Test for a reboot,  if this is a reboot just skip this script.
#
if test "$RS_REBOOT" = "true" ; then
  echo "Skip code install on reboot."
  logger -t RightScale "Skip code install on reboot."
  exit 0 # Leave with a smile ...
fi

## set hostname
hostname $HOSTNAME

## move to deploy_dir
cd $DEPLOY_DIR

## move settings_production.py to settings_local.py
mv -f settings_production.py settings_local.py

## fix newlines
flip -u manage.py

## fix exec
chmod +x cron/chronograph.sh

## setup the virtualenv
echo "Setting up virtualenv $DEPLOY_DIR/../pinax-env"
python lib/pinax/scripts/pinax-boot.py --development --source=lib/pinax ../pinax-env

## and make sure we are using it
echo "Activating virtualenv $DEPLOY_DIR/../pinax-env"
source ../pinax-env/bin/activate

## install deps for dev version
pip install --no-deps --requirement lib/pinax/requirements/external_apps.txt

## upgrade to django 1.1
pip install -U Django==1.1.1

## add boto
echo "Installing boto..."
easy_install boto

## build_media
echo "gathering static media..."
python manage.py build_media --all

## add PIL
echo "Installing python-imaging..."
sudo apt-get install python-imaging

## syncdb
echo "Syncing database..."
python manage.py syncdb --noinput

## chown
echo "Changing ownership to $APP_OWNER..."
chown -R $APP_OWNER $DEPLOY_DIR
if [ ! $? ]; then
  echo "Failed to change the owner."
  exit -1
fi

exit 0