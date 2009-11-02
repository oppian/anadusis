#!/bin/bash

DB_NAME=anadusis
FILENAME=$DB_NAME-db-`date +%Y%m%d%H%M`
BUCKET=anadusis-db-backups
export AWS_SECRET_ACCESS_KEY=U0MlBi5bACqK0qHRLEgH0WNFliebSS1xSwbr3wh2
export AWS_ACCESS_KEY_ID=AKIAI5KRE2OCDICYSLFA

if [ "$1" != "" ]; then
        FILENAME=$1
fi

# dump to filename
sudo -u postgres pg_dump -Fc $DB_NAME > /tmp/$FILENAME

# save to s3
s3cmd put $BUCKET:$FILENAME /tmp/$FILENAME

echo "Saved database '$DB_NAME' to $BUCKET:$FILENAME"

# delete tmp file
rm /tmp/$FILENAME
