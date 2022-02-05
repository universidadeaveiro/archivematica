#!/bin/sh

mkdir -p /var/archivematica/sharedDirectory
chown -R archivematica:archivematica /var/archivematica/sharedDirectory
su archivematica

su archivematica --command "/usr/local/bin/gunicorn --config=/src/src/dashboard/install/dashboard.gunicorn-config.py wsgi:application"
