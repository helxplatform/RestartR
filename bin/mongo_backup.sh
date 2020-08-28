#!/bin/sh
set -x
backup_date=`date +'%m-%d-%Y'`

cd /data/backup

rm -rf backup-*

mkdir backup-$backup_date

mongodump --host restartr-api-service --port $1 --username $2 --password $3 --out /data/backup/backup-$backup_date/dump





