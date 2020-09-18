#!/bin/sh
set -x
backup_date=`date +'%m-%d-%Y'`

cd /data/backup

if [ -d mongo_backups ]
then
  rm -rf mongo_backups
fi

mkdir mongo_backups
cd mongo_backups

mkdir backup-$backup_date

mongodump --host restartr-api-service --port 27017 --username $1 --password $2 --out /data/backup/mongo_backups/backup-$backup_date/dump





