#!/bin/bash -e
#
# Installs the cron file
#
# APP_OWNER - user cron runs as
# CRON_FILE - file for input to cron 
# DEPLOY_DIR - Installed directory

if test "$RS_REBOOT" = "true" ; then
  echo "Skip cron re-configuration on a reboot."
  exit 0 # Leave with a smile ...
fi

filename=`basename $CRON_FILE .cron`

# copy config
cp -f ${DEPLOY_DIR}${CRON_FILE} /etc/cron.d/$filename.tmp

# replace token
sed -i -e "s|@DEPLOY_DIR@|$DEPLOY_DIR|" /etc/cron.d/$filename.tmp
sed -i -e "s|@APP_OWNER@|$APP_OWNER|" /etc/cron.d/$filename.tmp

# fix newlines
cd /etc/cron.d
tr -d '\r' < $filename.tmp > $filename
rm $filename.tmp

exit 0