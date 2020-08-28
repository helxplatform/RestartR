#!/bin/bash
set -x
backup_date=`date +'%m-%d-%Y'`

cd /data/backup

if [ -d mongo_backups ]
then
  rm -rf backup-*
fi
mkdir mongo_backups && cd mongo_backups
mkdir backup-$backup_date && cd backup-$backup_date
mkdir dump && cd dump

mongodump --host restartr-api-service --port 27017 --username $1 --password $2 --out /data/backup/backup-$backup_date/dump





